# 🎯 Skill Manager - AI-Powered Career Development Platform

An intelligent skill management platform that uses AI to help users track their skills, identify gaps for target roles, and receive personalized learning recommendations.

## 🌟 Features

- **User & Skill Management**: Create profiles and track skill proficiency (1-5 levels)
- **Certifications**: Add professional certifications with issuer and date information
- **Achievements**: Document your accomplishments and projects
- **AI-Powered Gap Analysis**: Let AI analyze your complete profile against target roles
- **Smart Recommendations**: Get personalized course suggestions based on your background
- **Self-Assessment Quizzes**: Take AI-generated quizzes to evaluate your skills
- **Study Plans**: Receive customized learning roadmaps
- **Interactive Dashboard**: Clean Streamlit UI for easy interaction

## 🏗️ Architecture

- **Backend**: FastAPI (Python 3.10+)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Streamlit
- **AI**: Groq SDK (llama-3.3-70b-versatile model)
- **Testing**: pytest

## 📋 Prerequisites

- Python 3.10 or higher
- Groq API key (get one at [console.groq.com](https://console.groq.com))

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (or extract the project)
cd skill-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_groq_api_key_here
```

### 3. Initialize Database

```bash
# Seed database with default data
python scripts/seed_db.py
```

### 4. Run Backend

```bash
# Start FastAPI server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5. Run Frontend

```bash
# In a new terminal, activate venv and run Streamlit
streamlit run app/frontend/streamlit_app.py
```

The frontend will open at `http://localhost:8501`

## 📚 API Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "name": "John Doe"
  }'
```

### Add a Skill

```bash
curl -X POST "http://localhost:8000/skills/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "python",
    "level": 3
  }'
```

### Add a Certification

```bash
curl -X POST "http://localhost:8000/certifications/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AWS Certified Solutions Architect",
    "issuer": "Amazon Web Services",
    "date_obtained": "March 2024"
  }'
```

### Add an Achievement

```bash
curl -X POST "http://localhost:8000/achievements/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Led ML Pipeline Migration",
    "description": "Successfully migrated legacy ML pipeline to cloud-native architecture, reducing costs by 40%",
    "date": "2024"
  }'
```

### Get User with Skills

```bash
curl "http://localhost:8000/users/1"
```

### List Available Roles

```bash
curl "http://localhost:8000/roles/"
```

### Perform Skill Gap Analysis

```bash
curl -X POST "http://localhost:8000/analysis/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "role": "Data Scientist"
  }'
```

**Example AI Response:**

The AI now analyzes your complete profile including skills, certifications, and achievements to provide a comprehensive assessment:

```json
{
  "analysis": {
    "missing": ["deep_learning", "nlp"],
    "underdeveloped": [
      {
        "skill": "statistics",
        "user_level": 2,
        "required": 4,
        "severity": 2
      }
    ],
    "fit_score": 72,
    "overall_assessment": "Strong foundation with Python and ML certifications. Recent achievement in ML pipeline shows practical experience. Focus on statistics and deep learning to become fully qualified."
  },
  "recommendations": [
    {
      "title": "Deep Learning Specialization",
      "provider": "DeepLearning.AI",
      "level": "advanced",
      "related_skill": "ml",
      "reason": "Your ML pipeline achievement shows you're ready for advanced concepts. This will fill the deep learning gap."
    },
    {
      "title": "Statistics for Data Science",
      "provider": "Khan Academy",
      "level": "intermediate",
      "related_skill": "statistics",
      "reason": "Critical foundation needed to reach the required level 4 proficiency"
    }
  ],
  "study_plan": "Week 1-2: Complete Statistics for Data Science course to strengthen fundamentals. Week 3-6: Deep Learning Specialization - leverage your existing ML knowledge. Week 7-8: Apply deep learning to a project similar to your ML pipeline achievement to solidify learning.",
  "ai_used": true
}
```

### Generate Quiz

```bash
curl "http://localhost:8000/quiz/python"
```

### Submit Quiz Answers

```bash
curl -X POST "http://localhost:8000/quiz/python/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [0, 1, 2, 1]
  }'
```

## 🧪 Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_analysis.py -v

# Run with coverage
pytest --cov=app tests/
```

## 📁 Project Structure

```
skill-manager/
├── app/
│   ├── main.py              # FastAPI application
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── ai_client.py         # Groq AI integration
│   ├── routes/              # API endpoints
│   │   ├── users.py
│   │   ├── skills.py
│   │   ├── certifications.py
│   │   ├── achievements.py
│   │   ├── roles.py
│   │   ├── courses.py
│   │   ├── analysis.py
│   │   └── quiz.py
│   └── frontend/
│       └── streamlit_app.py # Streamlit UI
├── seed/
│   ├── roles.json           # Default roles
│   └── courses.json         # Default courses
├── scripts/
│   └── seed_db.py           # Database seeding script
├── tests/
│   ├── test_analysis.py     # Analysis tests
│   └── test_quiz.py         # Quiz tests
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎨 Frontend Features

The Streamlit interface provides:

1. **User Management**: Create/load user profiles
2. **Skills Tab**: Add, update, and delete skills with level sliders
3. **Certifications & Achievements Tab**: Document your professional credentials and accomplishments
4. **Gap Analysis Tab**: Select any role and get AI-powered comprehensive profile analysis
5. **Self-Assessment Tab**: Take AI-generated quizzes for any skill
6. **Courses Tab**: Browse available learning resources

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | SQLite database path | No (default: sqlite:///./dev.db) |
| GROQ_API_KEY | Groq API key for AI features | Yes (for AI features) |
| SECRET_KEY | Application secret key | No |

## 🎯 Default Roles

The system comes pre-configured with:

- **Data Scientist**: Python (4), ML (4), Statistics (3), SQL (3)
- **Backend Engineer**: Python (4), Databases (4), API (3)
- **Frontend Engineer**: JavaScript (4), React (4), CSS (3)

## 📖 Available Courses

12 pre-loaded courses covering:
- Python (beginner to advanced)
- Machine Learning
- Statistics
- SQL & Databases
- API Design
- JavaScript & React
- CSS

## 🤖 AI Features

### How AI Analysis Works

The system now uses a **conversational AI approach** instead of rigid requirements matching:

1. **Comprehensive Profile Analysis**: AI reviews your skills, certifications, and achievements together
2. **Contextual Understanding**: AI considers how your certifications validate your skills and how achievements demonstrate practical application
3. **Natural Assessment**: Instead of strict numerical requirements, AI provides nuanced evaluation based on the target role's actual needs
4. **Personalized Recommendations**: Course suggestions consider your existing knowledge and learning trajectory
5. **Custom Roles**: You can analyze your fit for any role, not just pre-defined ones

### Without GROQ_API_KEY
If the API key is not configured, AI endpoints will return:
```json
{
  "error": "GROQ_API_KEY not configured"
}
```

### With GROQ_API_KEY
- Intelligent profile analysis considering all credentials
- Context-aware gap identification
- Personalized course recommendations that build on existing knowledge
- Realistic, phased study plans
- Dynamic quiz generation
- Automatic scoring and level suggestions

## 🔧 Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available

### AI features not working
- Verify GROQ_API_KEY is set in `.env`
- Check API key is valid at console.groq.com
- Ensure you have API credits

### Database errors
- Delete `dev.db` and run `python scripts/seed_db.py` again
- Check file permissions in the project directory

## 📝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI powered by [Groq](https://groq.com/)
- UI built with [Streamlit](https://streamlit.io/)

---

**Happy Learning! 🚀**