"""Courses routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/", response_model=List[schemas.Course])
def list_courses(db: Session = Depends(get_db)):
    """List all available courses."""
    return crud.get_courses(db)


@router.post("/", response_model=schemas.Course, status_code=201)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """Add a new course."""
    return crud.create_course(db=db, course=course)