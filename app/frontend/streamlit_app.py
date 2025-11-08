"""Streamlit frontend for Skill Manager."""
import streamlit as st
import requests
from typing import Optional

# Page config
st.set_page_config(
    page_title="Skill Manager",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://localhost:8000"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None


def api_call(method: str, endpoint: str, data: Optional[dict] = None):
    """Make API call to backend."""
    url = f"{st.session_state.backend_url}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json() if response.text else None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


def main():
    """Main application."""
    st.title("🎯 AI-Powered Skill Manager")
    st.markdown("---")

    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        backend_url = st.text_input(
            "Backend URL",
            value=st.session_state.backend_url,
            help="URL of the FastAPI backend"
        )
        if backend_url != st.session_state.backend_url:
            st.session_state.backend_url = backend_url
            st.rerun()

        st.markdown("---")
        st.header("👤 User Management")

        # Create user
        with st.expander("Create New User"):
            email = st.text_input("Email")
            name = st.text_input("Name")
            if st.button("Create User"):
                result = api_call("POST", "/users/", {"email": email, "name": name})
                if result:
                    st.success(f"User created! ID: {result['id']}")
                    st.session_state.user_id = result["id"]

        # Get user
        user_id_input = st.number_input("User ID", min_value=1, value=1)
        if st.button("Load User"):
            result = api_call("GET", f"/users/{user_id_input}")
            if result:
                st.session_state.user_id = result["id"]
                st.session_state.user_data = result
                st.success(f"Loaded user: {result['name']}")

    # Main content
    if st.session_state.user_data:
        user = st.session_state.user_data

        # Display user info
        col1, col2 = st.columns([2, 1])
        with col1:
            st.header(f"Welcome, {user['name']}! 👋")
            st.write(f"**Email:** {user['email']}")
        with col2:
            if st.button("🔄 Refresh Profile"):
                result = api_call("GET", f"/users/{user['id']}")
                if result:
                    st.session_state.user_data = result
                    st.rerun()

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 My Skills", "🎓 Certifications & Achievements", "🎯 Gap Analysis", "📝 Self-Assessment", "📖 Courses"])

        # Tab 1: Skills Management
        with tab1:
            st.subheader("Your Skills")
            
            # Add new skill
            with st.expander("➕ Add New Skill"):
                col1, col2 = st.columns(2)
                with col1:
                    skill_name = st.text_input("Skill Name")
                with col2:
                    skill_level = st.slider("Level", 1, 5, 3)
                if st.button("Add Skill"):
                    result = api_call(
                        "POST",
                        f"/skills/users/{user['id']}",
                        {"name": skill_name, "level": skill_level}
                    )
                    if result:
                        st.success("Skill added!")
                        st.rerun()

            # Display skills
            if user.get("skills"):
                for skill in user["skills"]:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{skill['name']}**")
                    with col2:
                        new_level = st.slider(
                            f"Level###{skill['id']}",
                            1, 5,
                            skill['level'],
                            key=f"skill_{skill['id']}"
                        )
                        if new_level != skill['level']:
                            api_call("PUT", f"/skills/{skill['id']}", {"level": new_level})
                            st.success("Updated!")
                            st.rerun()
                    with col3:
                        if st.button("🗑️", key=f"del_{skill['id']}"):
                            api_call("DELETE", f"/skills/{skill['id']}")
                            st.rerun()
            else:
                st.info("No skills added yet. Add your first skill above!")

        # Tab 2: Certifications & Achievements
        with tab2:
            col1, col2 = st.columns(2)
            
            # Certifications
            with col1:
                st.subheader("🎓 Certifications")
                
                with st.expander("➕ Add Certification"):
                    cert_name = st.text_input("Certification Name")
                    cert_issuer = st.text_input("Issuer/Organization")
                    cert_date = st.text_input("Date Obtained (e.g., Jan 2024)")
                    if st.button("Add Certification"):
                        result = api_call(
                            "POST",
                            f"/certifications/users/{user['id']}",
                            {
                                "name": cert_name,
                                "issuer": cert_issuer,
                                "date_obtained": cert_date
                            }
                        )
                        if result:
                            st.success("Certification added!")
                            st.rerun()
                
                # Display certifications
                if user.get("certifications"):
                    for cert in user["certifications"]:
                        with st.container():
                            col_a, col_b = st.columns([4, 1])
                            with col_a:
                                st.write(f"**{cert['name']}**")
                                st.caption(f"{cert['issuer']} • {cert['date_obtained']}")
                            with col_b:
                                if st.button("🗑️", key=f"del_cert_{cert['id']}"):
                                    api_call("DELETE", f"/certifications/{cert['id']}")
                                    st.rerun()
                            st.markdown("---")
                else:
                    st.info("No certifications added yet.")
            
            # Achievements
            with col2:
                st.subheader("🏆 Achievements")
                
                with st.expander("➕ Add Achievement"):
                    achievement_title = st.text_input("Achievement Title")
                    achievement_desc = st.text_area("Description")
                    achievement_date = st.text_input("Date (e.g., 2024)")
                    if st.button("Add Achievement"):
                        result = api_call(
                            "POST",
                            f"/achievements/users/{user['id']}",
                            {
                                "title": achievement_title,
                                "description": achievement_desc,
                                "date": achievement_date
                            }
                        )
                        if result:
                            st.success("Achievement added!")
                            st.rerun()
                
                # Display achievements
                if user.get("achievements"):
                    for achievement in user["achievements"]:
                        with st.container():
                            col_a, col_b = st.columns([4, 1])
                            with col_a:
                                st.write(f"**{achievement['title']}**")
                                st.caption(f"{achievement['description']}")
                                st.caption(f"📅 {achievement['date']}")
                            with col_b:
                                if st.button("🗑️", key=f"del_ach_{achievement['id']}"):
                                    api_call("DELETE", f"/achievements/{achievement['id']}")
                                    st.rerun()
                            st.markdown("---")
                else:
                    st.info("No achievements added yet.")

        # Tab 3: Gap Analysis
        with tab3:
            st.subheader("AI-Powered Skill Gap Analysis")
            
            st.info("💡 The AI will analyze your complete profile (skills, certifications, and achievements) to assess your readiness for the target role.")
            
            # Get roles
            roles = api_call("GET", "/roles/")
            if roles:
                role_names = [role["name"] for role in roles]
                selected_role = st.selectbox("Select Target Role", role_names)
                
                # Allow custom role input
                use_custom = st.checkbox("Or enter a custom role")
                if use_custom:
                    selected_role = st.text_input("Custom Role Name", value="Machine Learning Engineer")
                
                if st.button("🔍 Analyze Skill Gap", type="primary"):
                    with st.spinner("AI is analyzing your complete profile..."):
                        result = api_call(
                            "POST",
                            "/analysis/",
                            {"user_id": user["id"], "role": selected_role}
                        )
                        
                        if result:
                            if "error" in result:
                                st.error(result["error"])
                            else:
                                # Display analysis
                                st.success("Analysis Complete!")
                                
                                analysis = result.get("analysis", {})
                                
                                # Fit score
                                fit_score = analysis.get("fit_score", 0)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Overall Fit Score", f"{fit_score}%")
                                with col2:
                                    if analysis.get("overall_assessment"):
                                        st.info(f"**Assessment:** {analysis['overall_assessment']}")
                                
                                # Missing skills
                                if analysis.get("missing"):
                                    st.warning("**Missing Skills:**")
                                    for skill in analysis["missing"]:
                                        st.write(f"- {skill}")
                                
                                # Underdeveloped skills
                                if analysis.get("underdeveloped"):
                                    st.warning("**Skills to Improve:**")
                                    for skill in analysis["underdeveloped"]:
                                        st.write(
                                            f"- {skill['skill']}: Level {skill['user_level']} → "
                                            f"{skill['required']} (Gap: {skill['severity']})"
                                        )
                                
                                # Recommendations
                                st.subheader("📚 Recommended Courses")
                                recommendations = result.get("recommendations", [])
                                if recommendations:
                                    for rec in recommendations:
                                        with st.expander(f"📖 {rec['title']}"):
                                            st.write(f"**Provider:** {rec['provider']}")
                                            st.write(f"**Level:** {rec['level']}")
                                            st.write(f"**Skill:** {rec['related_skill']}")
                                            st.write(f"**Why:** {rec['reason']}")
                                else:
                                    st.success("Great! You're well-prepared for this role.")
                                
                                # Study plan
                                st.subheader("📅 Personalized Study Plan")
                                st.info(result.get("study_plan", ""))

        # Tab 4: Self-Assessment
        with tab4:
            st.subheader("AI-Generated Self-Assessment Quiz")
            
            if user.get("skills"):
                skill_names = [skill["name"] for skill in user["skills"]]
                quiz_skill = st.selectbox("Select Skill to Test", skill_names)
                
                if st.button("📝 Generate Quiz", type="primary"):
                    with st.spinner("AI is generating questions..."):
                        quiz = api_call("GET", f"/quiz/{quiz_skill}")
                        
                        if quiz:
                            if "error" in quiz:
                                st.error(quiz["error"])
                            else:
                                st.session_state.current_quiz = quiz
                                st.session_state.quiz_skill = quiz_skill
                                st.rerun()
                
                # Display quiz
                if "current_quiz" in st.session_state:
                    quiz = st.session_state.current_quiz
                    st.write(f"**Quiz for: {quiz['skill']}**")
                    st.info("Answer all questions and click Submit to see your results.")
                    
                    answers = []
                    for i, q in enumerate(quiz["questions"]):
                        st.write(f"\n**Question {i+1}** ({q['difficulty']})")
                        st.write(q["q"])
                        answer = st.radio(
                            "Select answer:",
                            options=range(len(q["options"])),
                            format_func=lambda x, opts=q["options"]: opts[x],
                            key=f"q_{i}"
                        )
                        answers.append(answer)
                    
                    if st.button("✅ Submit Quiz"):
                        result = api_call(
                            "POST",
                            f"/quiz/{st.session_state.quiz_skill}/submit",
                            {"answers": answers}
                        )
                        
                        if result:
                            if "error" in result:
                                st.error(result["error"])
                            else:
                                # Store results for display
                                st.session_state.quiz_results = result
                                del st.session_state.current_quiz
                                del st.session_state.quiz_skill
                                st.rerun()
                
                # Display quiz results
                if "quiz_results" in st.session_state:
                    result = st.session_state.quiz_results
                    
                    st.success("✅ Quiz Submitted!")
                    
                    # Overall metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Your Score", f"{result['score']}%")
                    with col2:
                        st.metric("Suggested Level", f"{result['suggested_level']}/5")
                    
                    st.markdown("---")
                    
                    # Detailed results
                    st.subheader("📊 Detailed Results")
                    
                    if result.get("detailed_results"):
                        for item in result["detailed_results"]:
                            if item["is_correct"]:
                                st.success(f"**Question {item['question_number']}** ✓ Correct ({item['difficulty']})")
                            else:
                                st.error(f"**Question {item['question_number']}** ✗ Incorrect ({item['difficulty']})")
                            
                            st.write(f"**Q:** {item['question']}")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if item["is_correct"]:
                                    st.write(f"✅ **Your answer:** {item['user_answer']}")
                                else:
                                    st.write(f"❌ **Your answer:** {item['user_answer']}")
                            with col_b:
                                if not item["is_correct"]:
                                    st.write(f"✓ **Correct answer:** {item['correct_answer']}")
                            
                            st.markdown("---")
                    
                    # Option to take another quiz
                    if st.button("🔄 Take Another Quiz"):
                        del st.session_state.quiz_results
                        st.rerun()
                        
            else:
                st.info("Add some skills first to take quizzes!")

        # Tab 5: Courses
        with tab5:
            st.subheader("Available Courses")
            courses = api_call("GET", "/courses/")
            if courses:
                for course in courses:
                    with st.expander(f"📖 {course['title']}"):
                        st.write(f"**Provider:** {course['provider']}")
                        st.write(f"**Level:** {course['level']}")
                        st.write(f"**Related Skill:** {course['related_skill']}")

    else:
        st.info("👈 Please load or create a user from the sidebar to get started!")


if __name__ == "__main__":
    main()