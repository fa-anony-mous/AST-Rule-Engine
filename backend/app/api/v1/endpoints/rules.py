from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleResponse, RuleEvaluate
from app.services.rule_engine import evaluate_rule

router = APIRouter()

async def get_a_rule(db: AsyncSession, rule_id: int):
    result = await db.execute(select(Rule).filter(Rule.id == rule_id))
    rule = result.scalars().first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule

@router.get("/")
async def get_rules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule))
    rules = result.scalars().all()
    return {"rules": rules}

@router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_a_rule(db, rule_id)
    except Exception as e:
        print(f"Error fetching rule: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/", response_model=RuleResponse)
async def create_rule(rule_data: RuleCreate, db: AsyncSession = Depends(get_db)):
    """Create a new rule"""
    new_rule = Rule(**rule_data.model_dump())
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)
    return new_rule

@router.put("/{rule_id}", response_model=RuleResponse)
async def update_rule(rule_id: int, rule_data: RuleCreate, db: AsyncSession = Depends(get_db)):
    rule = await get_a_rule(db, rule_id)
    for key, value in rule_data.model_dump().items():
        setattr(rule, key, value)
    await db.commit()
    await db.refresh(rule)
    return rule

@router.post("/evaluate", response_model=dict)
async def evaluate_rule_endpoint(input_model: RuleEvaluate, db: AsyncSession = Depends(get_db)):
    """Evaluate a rule based on input data"""
    print(f"Received rule_id: {input_model.rule_id}, input_data: {input_model.input_data}")
    rule = await get_a_rule(db, input_model.rule_id)

    result = evaluate_rule(rule, input_model.input_data)

    return {"result": result}

@router.delete("/{rule_id}", status_code=204)
async def delete_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    rule = await get_a_rule(db, rule_id)
    await db.delete(rule)
    await db.commit()
    return

