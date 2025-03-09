from pydantic import BaseModel
from typing import Optional

class RuleBase(BaseModel):
    name: str
    description: str
    code: str
    is_active: Optional[bool] = True

class RuleResponse(RuleBase):
    id: int
    is_active: bool
    

class RuleCreate(RuleBase):
    pass

class RuleUpdate(RuleBase):
    pass

class RuleEvaluate(BaseModel):
    rule_id: int
    input_data: dict




