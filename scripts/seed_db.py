"""Database seeding script."""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db import SessionLocal, init_db
from app import models

def seed_database():
    """Seed the database with initial data."""
    init_db()
    db = SessionLocal()

    try:
        # Create default user
        existing_user = db.query(models.User).filter_by(email="user@mail.com").first()
        if not existing_user:
            user = models.User(email="user@mail.com", name="Demo User")
            db.add(user)
            print("✓ Created default user")
        else:
            print("✓ Default user already exists")

        # Load and create roles
        roles_file = Path(__file__).parent.parent / "seed" / "roles.json"
        with open(roles_file, "r") as f:
            roles_data = json.load(f)

        for role_data in roles_data:
            existing_role = db.query(models.Role).filter_by(name=role_data["name"]).first()
            if not existing_role:
                role = models.Role(
                    name=role_data["name"],
                    requirements=role_data["requirements"]
                )
                db.add(role)
                print(f"✓ Created role: {role_data['name']}")
            else:
                print(f"✓ Role already exists: {role_data['name']}")

        # Load and create courses
        courses_file = Path(__file__).parent.parent / "seed" / "courses.json"
        with open(courses_file, "r") as f:
            courses_data = json.load(f)

        for course_data in courses_data:
            existing_course = db.query(models.Course).filter_by(
                title=course_data["title"]
            ).first()
            if not existing_course:
                course = models.Course(**course_data)
                db.add(course)
                print(f"✓ Created course: {course_data['title']}")
            else:
                print(f"✓ Course already exists: {course_data['title']}")

        db.commit()
        print("\n✅ Database seeding completed successfully!")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()