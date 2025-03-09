import ast
import operator

import sys 
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.models.rule import Rule



# Define supported operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Gt: operator.gt,
    ast.Lt: operator.lt,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.GtE: operator.ge,
    ast.LtE: operator.le,
    ast.And: lambda a, b: a and b,  # Logical AND
    ast.Or: lambda a, b: a or b,    # Logical OR
}

def evaluate_expression(node, input_data):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.BinOp):  # Binary operations (e.g., x + y)
        left = evaluate_expression(node.left, input_data)
        right = evaluate_expression(node.right, input_data)
        return operators[type(node.op)](left, right)
    elif isinstance(node, ast.Compare):  # Comparison operations (e.g., x <= 10)
        left = evaluate_expression(node.left, input_data)
        for op, comparator in zip(node.ops, node.comparators):
            right = evaluate_expression(comparator, input_data)
            if not operators[type(op)](left, right):
                return False
            left = right  # For chained comparisons (e.g., 1 < x < 10)
        return True
    elif isinstance(node, ast.BoolOp):  # Logical operations (e.g., x > 10 and x <= 20)
        values = [evaluate_expression(value, input_data) for value in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        elif isinstance(node.op, ast.Or):
            return any(values)
        else:
            raise ValueError(f"Unsupported BoolOp: {type(node.op)}")
    elif isinstance(node, ast.Constant):  # Numbers
        return node.n
    elif isinstance(node, ast.Constant):  # Strings
        return node.s
    elif isinstance(node, ast.Name):  # Variable names
        return input_data[node.id]
    elif isinstance(node, ast.Constant):  # Constants (Python 3.8+)
        return node.value
    else:
        raise ValueError(f"Unsupported AST node: {ast.dump(node)}")

def evaluate_rule(rule: Rule, input_data: dict) -> bool:
    """Evaluate the rule against the provided input data."""
    try:
        # Parse the rule code into an AST
        tree = ast.parse(rule.code, mode='eval')
        
        # Evaluate the expression
        result = evaluate_expression(tree.body, input_data)
        
        return result
    except Exception as e:
        raise ValueError(f"Error evaluating rule: {str(e)}") 