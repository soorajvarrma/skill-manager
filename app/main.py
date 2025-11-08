"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routes import users, skills, roles, courses, analysis, quiz, certifications, achievements

# Initialize database
init_db()

app = FastAPI(
    title="Skill Manager API",
    description="AI-powered skill management and career development platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(skills.router)
app.include_router(certifications.router)
app.include_router(achievements.router)
app.include_router(roles.router)
app.include_router(courses.router)
app.include_router(analysis.router)
app.include_router(quiz.router)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Skill Manager API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users/",
            "skills": "/skills/",
            "certifications": "/certifications/",
            "achievements": "/achievements/",
            "roles": "/roles/",
            "courses": "/courses/",
            "analysis": "/analysis/",
            "quiz": "/quiz/{skill}",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}