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
        # Store quiz data for later scoring
        active_quizzes[skill] = {
            "correct_answers": [q["correct"] for q in result["questions"]],
            "questions": result["questions"]
        }
    
    return result


@router.post("/{skill}/submit")
def submit_quiz(skill: str, submission: schemas.QuizSubmission):
    """
    Submit quiz answers and receive detailed score with correct answers.
    
    Shows score percentage, recommended skill level, and breakdown of
    wrong answers with correct solutions.
    """
    if not ai_client.is_configured():
        return {"error": "GROQ_API_KEY not configured"}

    if skill not in active_quizzes:
        return {"error": "No active quiz found for this skill. Generate a quiz first."}

    quiz_data = active_quizzes[skill]
    correct_answers = quiz_data["correct_answers"]
    questions = quiz_data["questions"]
    
    result = ai_client.score_quiz(submission.answers, correct_answers, questions)
    
    # Clean up
    del active_quizzes[skill]
    
    return result