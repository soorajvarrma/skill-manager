"""Skills routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("/users/{user_id}", response_model=schemas.Skill, status_code=201)
def add_skill(user_id: int, skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    """Add a skill to a user."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_skill(db=db, skill=skill, user_id=user_id)


@router.put("/{skill_id}", response_model=schemas.Skill)
def update_skill(skill_id: int, skill: schemas.SkillUpdate, db: Session = Depends(get_db)):
    """Update skill level."""
    db_skill = crud.update_skill(db, skill_id=skill_id, skill_update=skill)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill


@router.delete("/{skill_id}", status_code=204)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    """Delete a skill."""
    success = crud.delete_skill(db, skill_id=skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return None