# 🎯 Skill Manager - AI-Powered Career Development Platform

An intelligent skill management platform that uses AI to help users track their skills, identify gaps for target roles, and receive personalized learning recommendations.

## 🌟 Features

- **User & Skill Management**: Create profiles and track skill proficiency (1-5 levels)
- **AI-Powered Gap Analysis**: Compare your skills against target roles using Groq AI
- **Smart Recommendations**: Get personalized course suggestions based on your gaps
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

```json
{
  "analysis": {
    "missing": ["ml", "statistics"],
    "underdeveloped": [
      {
        "skill": "python",
        "user_level": 3,
        "required": 4,
        "severity": 1
      }
    ],
    "fit_score": 65
  },
  "recommendations": [
    {
      "title": "Machine Learning Fundamentals",
      "provider": "Coursera",
      "level": "intermediate",
      "related_skill": "ml",
      "reason": "Essential for data science roles"
    }
  ],
  "study_plan": "Week 1: Strengthen Python with advanced topics; Week 2-3: Complete ML fundamentals course; Week 4: Learn statistics basics",
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
3. **Gap Analysis Tab**: Select target role and get AI analysis
4. **Self-Assessment Tab**: Take AI-generated quizzes for any skill
5. **Courses Tab**: Browse available learning resources

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

### Without GROQ_API_KEY
If the API key is not configured, AI endpoints will return:
```json
{
  "error": "GROQ_API_KEY not configured"
}
```

### With GROQ_API_KEY
- Intelligent skill gap analysis
- Personalized course recommendations
- Context-aware study plans
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