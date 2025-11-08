"""Achievements routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.post("/users/{user_id}", response_model=schemas.Achievement, status_code=201)
def add_achievement(user_id: int, achievement: schemas.AchievementCreate, db: Session = Depends(get_db)):
    """Add an achievement to a user."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_achievement(db=db, achievement=achievement, user_id=user_id)


@router.delete("/{achievement_id}", status_code=204)
def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    """Delete an achievement."""
    success = crud.delete_achievement(db, achievement_id=achievement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return None