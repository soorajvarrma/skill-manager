"""CRUD operations for database models."""
from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user."""
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_skill(db: Session, skill: schemas.SkillCreate, user_id: int) -> models.Skill:
    """Create a new skill for a user."""
    db_skill = models.Skill(**skill.dict(), user_id=user_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def get_skill(db: Session, skill_id: int) -> Optional[models.Skill]:
    """Get skill by ID."""
    return db.query(models.Skill).filter(models.Skill.id == skill_id).first()


def update_skill(db: Session, skill_id: int, skill_update: schemas.SkillUpdate) -> Optional[models.Skill]:
    """Update skill level."""
    db_skill = get_skill(db, skill_id)
    if db_skill:
        db_skill.level = skill_update.level
        db.commit()
        db.refresh(db_skill)
    return db_skill


def delete_skill(db: Session, skill_id: int) -> bool:
    """Delete a skill."""
    db_skill = get_skill(db, skill_id)
    if db_skill:
        db.delete(db_skill)
        db.commit()
        return True
    return False


def create_role(db: Session, role: schemas.RoleCreate) -> models.Role:
    """Create a new role."""
    db_role = models.Role(name=role.name, requirements=role.requirements)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session) -> List[models.Role]:
    """Get all roles."""
    return db.query(models.Role).all()


def get_role_by_name(db: Session, name: str) -> Optional[models.Role]:
    """Get role by name."""
    return db.query(models.Role).filter(models.Role.name == name).first()


def create_course(db: Session, course: schemas.CourseCreate) -> models.Course:
    """Create a new course."""
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses(db: Session) -> List[models.Course]:
    """Get all courses."""
    return db.query(models.Course).all()


def create_certification(db: Session, certification: schemas.CertificationCreate, user_id: int) -> models.Certification:
    """Create a new certification for a user."""
    db_cert = models.Certification(**certification.dict(), user_id=user_id)
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert


def get_certification(db: Session, certification_id: int) -> Optional[models.Certification]:
    """Get certification by ID."""
    return db.query(models.Certification).filter(models.Certification.id == certification_id).first()


def delete_certification(db: Session, certification_id: int) -> bool:
    """Delete a certification."""
    db_cert = get_certification(db, certification_id)
    if db_cert:
        db.delete(db_cert)
        db.commit()
        return True
    return False


def create_achievement(db: Session, achievement: schemas.AchievementCreate, user_id: int) -> models.Achievement:
    """Create a new achievement for a user."""
    db_achievement = models.Achievement(**achievement.dict(), user_id=user_id)
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


def get_achievement(db: Session, achievement_id: int) -> Optional[models.Achievement]:
    """Get achievement by ID."""
    return db.query(models.Achievement).filter(models.Achievement.id == achievement_id).first()


def delete_achievement(db: Session, achievement_id: int) -> bool:
    """Delete an achievement."""
    db_achievement = get_achievement(db, achievement_id)
    if db_achievement:
        db.delete(db_achievement)
        db.commit()
        return True
    return False