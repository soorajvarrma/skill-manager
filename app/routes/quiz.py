"""Quiz routes for self-assessment."""
from fastapi import APIRouter
from app import schemas
from app.ai_client import ai_client

router = APIRouter(prefix="/quiz", tags=["quiz"])

# Store active quizzes in memory (in production, use Redis or database)
active_quizzes = {}


@router.get("/{skill}")
def generate_quiz(skill: str):
    """
    Generate an AI-powered self-assessment quiz for a skill.
    
    Returns 4 multiple-choice questions with varying difficulty levels.
    """
    if not ai_client.is_configured():
        return {"error": "GROQ_API_KEY not configured"}

    result = ai_client.generate_quiz(skill)
    
    if "error" not in result:
        # Store correct answers for later scoring
        active_quizzes[skill] = [q["correct"] for q in result["questions"]]
    
    return result


@router.post("/{skill}/submit")
def submit_quiz(skill: str, submission: schemas.QuizSubmission):
    """
    Submit quiz answers and receive score with suggested skill level.
    
    Compares submitted answers against correct answers and calculates
    a score percentage and recommended skill level.
    """
    if not ai_client.is_configured():
        return {"error": "GROQ_API_KEY not configured"}

    if skill not in active_quizzes:
        return {"error": "No active quiz found for this skill. Generate a quiz first."}

    correct_answers = active_quizzes[skill]
    result = ai_client.score_quiz(submission.answers, correct_answers)
    
    # Clean up
    del active_quizzes[skill]
    
    return result