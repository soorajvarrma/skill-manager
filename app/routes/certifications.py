"""Certifications routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/certifications", tags=["certifications"])


@router.post("/users/{user_id}", response_model=schemas.Certification, status_code=201)
def add_certification(user_id: int, certification: schemas.CertificationCreate, db: Session = Depends(get_db)):
    """Add a certification to a user."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_certification(db=db, certification=certification, user_id=user_id)


@router.delete("/{certification_id}", status_code=204)
def delete_certification(certification_id: int, db: Session = Depends(get_db)):
    """Delete a certification."""
    success = crud.delete_certification(db, certification_id=certification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Certification not found")
    return None