"""Roles routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[schemas.Role])
def list_roles(db: Session = Depends(get_db)):
    """List all available roles."""
    return crud.get_roles(db)


@router.post("/", response_model=schemas.Role, status_code=201)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """Create a new role with skill requirements."""
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db=db, role=role)