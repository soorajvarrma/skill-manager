"""AI client for Groq API integration."""
import os
import json
from typing import Dict, List, Any, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class AIClient:
    """Client for interacting with Groq API."""

    def __init__(self):
        """Initialize Groq client."""
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return self.api_key is not None and self.api_key != ""

    def generate_skill_gap_analysis(
        self,
        user_skills: List[Dict[str, Any]],
        user_certifications: List[Dict[str, str]],
        user_achievements: List[Dict[str, str]],
        target_role: str,
        course_catalog: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate skill gap analysis using Groq AI.
        
        Args:
            user_skills: List of user's current skills with levels
            user_certifications: List of user's certifications
            user_achievements: List of user's achievements
            target_role: Target job role name
            course_catalog: Available courses
            
        Returns:
            Analysis results with recommendations and study plan
        """
        if not self.is_configured():
            return {"error": "GROQ_API_KEY not configured"}

        # Format user profile
        skills_text = ", ".join([f"{s['name']} (Level {s['level']}/5)" for s in user_skills]) if user_skills else "None"
        
        certifications_text = ""
        if user_certifications:
            certifications_text = "\n".join([
                f"- {c['name']} from {c['issuer']} (obtained: {c['date_obtained']})"
                for c in user_certifications
            ])
        else:
            certifications_text = "None"
        
        achievements_text = ""
        if user_achievements:
            achievements_text = "\n".join([
                f"- {a['title']}: {a['description']} ({a['date']})"
                for a in user_achievements
            ])
        else:
            achievements_text = "None"

        # Format course catalog
        course_list = "\n".join([
            f"- {c['title']} by {c['provider']} ({c['level']}) - focuses on {c['related_skill']}"
            for c in course_catalog
        ])

        prompt = f"""You are an AI career advisor. Analyze this person's qualifications for the role of {target_role}.

**Current Profile:**

Skills: {skills_text}

Certifications:
{certifications_text}

Achievements:
{achievements_text}

**Target Role:** {target_role}

**Available Courses:**
{course_list}

Based on this information, assess how well this person fits the {target_role} role. Identify what skills are missing, what skills need improvement, and recommend specific courses from the available list(do not recommend any if the user doesnt need it) that would help bridge the gaps.

Provide your analysis as a JSON object with this EXACT structure:
{{
  "analysis": {{
    "missing": ["skill1", "skill2"],
    "underdeveloped": [
      {{"skill": "skillname", "user_level": 2, "required": 4, "severity": 2}}
    ],
    "fit_score": 65,
    "overall_assessment": "Brief assessment of their readiness"
  }},
  "recommendations": [
    {{"title": "Course Title", "provider": "Provider", "level": "beginner", "related_skill": "skill", "reason": "Why this course helps"}}
  ],
  "study_plan": "Week-by-week study plan with realistic timelines"
}}

Output ONLY the JSON, no other text or explanation."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )

            content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            result = json.loads(content)
            result["ai_used"] = True
            return result

        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "analysis": {"missing": [], "underdeveloped": [], "fit_score": 0},
                "recommendations": [],
                "study_plan": "Unable to generate study plan",
                "ai_used": False
            }

    def generate_quiz(self, skill: str) -> Dict[str, Any]:
        """
        Generate a self-assessment quiz for a skill.
        
        Args:
            skill: Skill name to generate quiz for
            
        Returns:
            Quiz with 4 multiple-choice questions
        """
        if not self.is_configured():
            return {"error": "GROQ_API_KEY not configured"}

        prompt = f"""Create 4 multiple-choice questions for the skill: {skill}. 
Each question has 4 options and one correct answer (index 0-3).
Output ONLY valid JSON:
{{
  "skill": "{skill}",
  "questions": [
    {{
      "q": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": 0,
      "difficulty": "beginner"
    }}
  ]
}}

Include a mix of difficulties: 1 beginner, 2 intermediate, 1 advanced.
Do not include commentary or explanations. Output valid JSON only."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1500
            )

            content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            result = json.loads(content)
            return result

        except Exception as e:
            return {"error": f"Quiz generation failed: {str(e)}"}

    def score_quiz(self, answers: List[int], correct_answers: List[int], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score quiz answers and suggest skill level.
        
        Args:
            answers: User's answers
            correct_answers: Correct answers
            questions: Original questions with options
            
        Returns:
            Score percentage, suggested skill level, and detailed results
        """
        correct_count = sum(1 for a, c in zip(answers, correct_answers) if a == c)
        total = len(correct_answers)
        score = int((correct_count / total) * 100)

        # Suggest skill level based on score
        if score >= 90:
            suggested_level = 5
        elif score >= 75:
            suggested_level = 4
        elif score >= 60:
            suggested_level = 3
        elif score >= 40:
            suggested_level = 2
        else:
            suggested_level = 1

        # Build detailed results
        detailed_results = []
        for i, (user_answer, correct_answer, question) in enumerate(zip(answers, correct_answers, questions)):
            is_correct = user_answer == correct_answer
            detailed_results.append({
                "question_number": i + 1,
                "question": question.get("q", ""),
                "user_answer": question.get("options", [])[user_answer] if user_answer < len(question.get("options", [])) else "Invalid",
                "correct_answer": question.get("options", [])[correct_answer] if correct_answer < len(question.get("options", [])) else "Unknown",
                "is_correct": is_correct,
                "difficulty": question.get("difficulty", "unknown")
            })

        return {
            "score": score,
            "suggested_level": suggested_level,
            "ai_used": True,
            "detailed_results": detailed_results
        }


# Global AI client instance
ai_client = AIClient()