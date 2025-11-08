"""Skill gap analysis routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db
from app.ai_client import ai_client

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/")
def analyze_skill_gap(request: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    """
    Perform AI-powered skill gap analysis.
    
    Analyzes user's complete profile (skills, certifications, achievements)
    against target role and generates personalized recommendations.
    """
    if not ai_client.is_configured():
        return {"error": "GROQ_API_KEY not configured"}

    # Get user with skills, certifications, and achievements
    user = crud.get_user(db, user_id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all courses
    courses = crud.get_courses(db)

    # Prepare data for AI
    user_skills = [{"name": skill.name, "level": skill.level} for skill in user.skills]
    
    user_certifications = [
        {
            "name": cert.name,
            "issuer": cert.issuer,
            "date_obtained": cert.date_obtained
        }
        for cert in user.certifications
    ]
    
    user_achievements = [
        {
            "title": achievement.title,
            "description": achievement.description,
            "date": achievement.date
        }
        for achievement in user.achievements
    ]
    
    course_catalog = [
        {
            "title": course.title,
            "provider": course.provider,
            "level": course.level,
            "related_skill": course.related_skill
        }
        for course in courses
    ]

    # Generate analysis using AI
    result = ai_client.generate_skill_gap_analysis(
        user_skills=user_skills,
        user_certifications=user_certifications,
        user_achievements=user_achievements,
        target_role=request.role,
        course_catalog=course_catalog
    )

    return result