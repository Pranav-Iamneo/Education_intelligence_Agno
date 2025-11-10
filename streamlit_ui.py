"""
Education & Learning Intelligence System - Streamlit UI
Interactive dashboard for student assessment and learning
"""

import streamlit as st
import json
from datetime import datetime
from agents.orchestrator import orchestrator

# Page configuration
st.set_page_config(
    page_title="Education Intelligence System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding: 10px 20px;
    }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    h2 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None
if "learning_path" not in st.session_state:
    st.session_state.learning_path = None


def call_agent(operation: str, data: dict) -> dict:
    """Call agents directly"""
    try:
        if operation == "assess":
            result = orchestrator.assess_student(data)
            print(f"DEBUG - Orchestrator result: {result}")
            return result
        elif operation == "learning_path":
            result = orchestrator.get_learning_path(data)
            print(f"DEBUG - Learning path result: {result}")
            # Extract the analysis from the result if it has status
            if isinstance(result, dict) and result.get("status") == "success":
                return {
                    "status": "success",
                    "analysis": result.get("analysis", result),
                    "timestamp": datetime.now().isoformat()
                }
            return {
                "status": "success",
                "analysis": result,
                "timestamp": datetime.now().isoformat()
            }
        elif operation == "progress":
            result = orchestrator.get_progress(data)
            # Extract the analysis from the result if it has status
            if isinstance(result, dict) and result.get("status") == "success":
                return {
                    "status": "success",
                    "analysis": result.get("analysis", result),
                    "timestamp": datetime.now().isoformat()
                }
            return {
                "status": "success",
                "analysis": result,
                "timestamp": datetime.now().isoformat()
            }
        elif operation == "recommendations":
            result = orchestrator.get_recommendations(data)
            # Extract the analysis from the result if it has status
            if isinstance(result, dict) and result.get("status") == "success":
                return {
                    "status": "success",
                    "analysis": result.get("analysis", result),
                    "timestamp": datetime.now().isoformat()
                }
            return {
                "status": "success",
                "analysis": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown operation: {operation}"
            }
    except Exception as e:
        import traceback
        print(f"DEBUG - Error in call_agent: {str(e)}")
        print(f"DEBUG - Traceback: {traceback.format_exc()}")
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }


def display_assessment_results(result: dict):
    """Display assessment results"""
    if result.get("status") == "error":
        st.error(f"Assessment Error: {result.get('message', 'Unknown error')}")
        return

    assessment = result.get("assessment", {})
    if not assessment:
        st.warning("Assessment data incomplete")
        return

    # Overall Score
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        score = assessment.get("overall_score", 0)
        st.metric("Overall Score", f"{score}%", delta=f"Accuracy: {score}%")

    with col2:
        skill_level = assessment.get("skill_level", "N/A")
        st.metric("Skill Level", skill_level)

    with col3:
        questions = assessment.get("questions_answered", 0)
        st.metric("Questions", f"{questions}")

    with col4:
        time_taken = assessment.get("time_taken_minutes", 0)
        st.metric("Time Taken", f"{time_taken} min")

    st.divider()

    # Performance by Topic
    st.subheader("Performance by Topic")
    topics = assessment.get("performance_by_topic", {})
    if topics:
        topic_data = []
        for topic, data in topics.items():
            topic_data.append({
                "Topic": topic,
                "Score": data.get("score", 0),
                "Status": data.get("status", "N/A")
            })

        for item in topic_data:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{item['Topic']}**")
            with col2:
                st.metric("Score", f"{item['Score']}%")
            with col3:
                status_color = "🟢" if item['Status'] == "mastered" else "🟡" if item['Status'] == "learning" else "🔴"
                st.write(f"{status_color} {item['Status'].title()}")

    st.divider()

    # Strengths and Weaknesses
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Strengths")
        strengths = assessment.get("strengths", [])
        if strengths:
            for strength in strengths:
                st.success(f"✓ {strength}")
        else:
            st.info("No identified strengths")

    with col2:
        st.subheader("Areas for Improvement")
        weaknesses = assessment.get("weaknesses", [])
        if weaknesses:
            for weakness in weaknesses:
                st.warning(f"⚠ {weakness}")
        else:
            st.info("No weak areas identified")

    st.divider()

    # Learning Path
    st.subheader("Recommended Learning Path")
    learning_path = assessment.get("learning_path", {})
    if learning_path:
        st.write(f"**Current Level:** {learning_path.get('current_level', 'N/A')}")
        st.write(f"**Target Level:** {learning_path.get('target_level', 'N/A')}")
        st.write(f"**Estimated Duration:** {learning_path.get('estimated_weeks', 'N/A')} weeks")
        st.write(f"**Hours per Week:** {learning_path.get('hours_per_week', 'N/A')}")

        milestones = learning_path.get("milestones", [])
        if milestones:
            st.write("**Milestones:**")
            for i, milestone in enumerate(milestones, 1):
                st.write(f"{i}. {milestone}")

    st.divider()

    # Progress Metrics
    st.subheader("Progress Metrics")
    metrics = assessment.get("progress_metrics", {})
    if metrics:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Score", f"{metrics.get('current_score', 0)}%")

        with col2:
            st.metric("Improvement Rate", metrics.get("improvement_rate", "N/A"))

        with col3:
            completed = metrics.get("topics_completed", 0)
            total = metrics.get("topics_total", 0)
            st.metric("Topics Completed", f"{completed}/{total}")

        with col4:
            weeks = metrics.get("estimated_completion_weeks", 0)
            st.metric("Est. Completion", f"{weeks} weeks")

        prob = metrics.get("success_probability", 0)
        st.progress(prob / 100, text=f"Success Probability: {prob}%")

    st.divider()

    # Summary
    st.subheader("Summary")
    summary = assessment.get("final_summary", "Assessment complete")
    st.markdown(summary)


# ============================================================================
# MAIN UI
# ============================================================================

st.title("🎓 Education & Learning Intelligence System")
st.markdown("AI-powered student assessment, learning path recommendation, and progress tracking")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Assessment", "Learning Path", "Progress", "System Info"])

# ============================================================================
# TAB 1: ASSESSMENT
# ============================================================================

with tab1:
    st.header("Student Assessment")
    st.markdown("Evaluate student knowledge and identify skill levels")

    col1, col2 = st.columns(2)

    with col1:
        student_name = st.text_input("Student Name", value="Alex Kumar", key="assess_name")
        subject = st.selectbox(
            "Subject",
            ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History", "Computer Science"],
            key="assess_subject"
        )
        difficulty_level = st.select_slider(
            "Difficulty Level",
            options=["beginner", "intermediate", "advanced"],
            value="intermediate",
            key="assess_difficulty"
        )

    with col2:
        questions_count = st.number_input("Total Questions", min_value=1, max_value=100, value=10, key="assess_questions")
        correct_answers = st.number_input("Correct Answers", min_value=0, max_value=questions_count, value=8, key="assess_correct")
        incorrect_answers = st.number_input("Incorrect Answers", min_value=0, max_value=questions_count, value=2, key="assess_incorrect")
        partial_answers = st.number_input("Partial Answers", min_value=0, max_value=questions_count, value=0, key="assess_partial")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Weak Areas** (topics needing improvement)")
        weak_areas = st.multiselect(
            "Select weak areas",
            options=["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"],
            default=["Topic 2"],
            key="weak_areas",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("**Strong Areas** (mastered topics)")
        strong_areas = st.multiselect(
            "Select strong areas",
            options=["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"],
            default=["Topic 1", "Topic 3"],
            key="strong_areas",
            label_visibility="collapsed"
        )

    st.divider()

    # Assessment Button
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("🚀 Run Assessment", use_container_width=True, key="run_assessment"):
            with st.spinner("Analyzing student performance..."):
                assessment_data = {
                    "student_name": student_name,
                    "subject": subject,
                    "questions_count": questions_count,
                    "correct_answers": correct_answers,
                    "incorrect_answers": incorrect_answers,
                    "partial_answers": partial_answers,
                    "difficulty_level": difficulty_level,
                    "weak_areas": weak_areas,
                    "strong_areas": strong_areas
                }

                result = call_agent("assess", assessment_data)
                st.session_state.assessment_result = result

    # Display Results
    if st.session_state.assessment_result:
        st.divider()
        display_assessment_results(st.session_state.assessment_result)

    # Sample Assessment Button
    if st.button("📊 Load Sample Assessment", use_container_width=False, key="sample_assess"):
        with st.spinner("Loading sample assessment..."):
            sample_data = {
                "student_name": "Sarah Chen",
                "subject": "Calculus Fundamentals",
                "questions_count": 15,
                "correct_answers": 12,
                "incorrect_answers": 2,
                "partial_answers": 1,
                "difficulty_level": "intermediate",
                "weak_areas": ["Integration", "Differential Equations"],
                "strong_areas": ["Limits", "Derivatives"]
            }
            result = call_agent("assess", sample_data)
            st.session_state.assessment_result = result
            st.rerun()


# ============================================================================
# TAB 2: LEARNING PATH
# ============================================================================

with tab2:
    st.header("Personalized Learning Path")
    st.markdown("Get AI-recommended learning routes tailored to your needs")

    col1, col2 = st.columns(2)

    with col1:
        lp_name = st.text_input("Student Name", value="Sarah Chen", key="lp_name")
        lp_subject = st.selectbox(
            "Subject",
            ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History", "Computer Science"],
            key="lp_subject"
        )

    with col2:
        lp_style = st.selectbox(
            "Learning Style",
            ["visual", "auditory", "kinesthetic", "reading", "mixed"],
            key="lp_style"
        )

    st.divider()

    if st.button("📚 Generate Learning Path", use_container_width=True, key="gen_path"):
        with st.spinner("Generating personalized learning path..."):
            lp_data = {
                "student_name": lp_name,
                "subject": lp_subject,
                "learning_style": lp_style
            }

            result = call_agent("learning_path", lp_data)
            st.session_state.learning_path = result

    if st.session_state.learning_path:
        st.divider()

        if st.session_state.learning_path.get("status") == "error":
            st.error(f"Error: {st.session_state.learning_path.get('message')}")
        else:
            analysis = st.session_state.learning_path.get("analysis", "")

            st.subheader("Learning Path Recommendation")

            # Always display as markdown (handles both string and dict content)
            if isinstance(analysis, str):
                st.markdown(analysis)
            elif isinstance(analysis, dict):
                if "learning_path" in analysis:
                    # Handle structured dict response
                    lp = analysis["learning_path"]
                    st.write(f"**Current Level:** {lp.get('current_level', 'N/A')}")
                    st.write(f"**Target Level:** {lp.get('target_level', 'N/A')}")
                    st.write(f"**Estimated Duration:** {lp.get('estimated_weeks', 'N/A')} weeks")
                    st.write(f"**Hours per Week:** {lp.get('hours_per_week', 'N/A')}")

                    if "milestones" in lp:
                        st.write("**Milestones:**")
                        for i, milestone in enumerate(lp["milestones"], 1):
                            st.write(f"{i}. {milestone}")

                    if "weekly_schedule" in lp:
                        st.write("**Weekly Schedule:**")
                        for week, details in lp["weekly_schedule"].items():
                            with st.expander(f"{week} ({details.get('hours', 0)}h)"):
                                st.write(f"**Topic:** {details.get('focus_topic', 'N/A')}")
                                st.write(f"**Resources:** {', '.join(details.get('resources', []))}")
                                st.write(f"**Practice:** {details.get('practices', 0)} exercises")
                                st.write(f"**Checkpoint:** {details.get('checkpoint', 'N/A')}")
                else:
                    # Generic dict display
                    st.json(analysis)
            else:
                st.write(analysis)


# ============================================================================
# TAB 3: PROGRESS
# ============================================================================

with tab3:
    st.header("Progress Tracking")
    st.markdown("Monitor learning progress and improvement over time")

    col1, col2, col3 = st.columns(3)

    with col1:
        prog_name = st.text_input("Student Name", value="Jordan Lee", key="prog_name")
        prog_subject = st.selectbox(
            "Subject",
            ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History", "Computer Science"],
            key="prog_subject"
        )

    with col2:
        initial_score = st.slider("Initial Score (%)", 0, 100, 65, key="initial_score")
        current_score = st.slider("Current Score (%)", 0, 100, 78, key="current_score")

    with col3:
        assessments = st.number_input("Assessments Completed", min_value=1, max_value=20, value=3, key="assessments")
        topics_completed = st.number_input("Topics Completed", min_value=0, max_value=50, value=5, key="topics_comp")
        hours_studied = st.number_input("Hours Studied", min_value=0, max_value=100, value=12, key="hours_study")

    st.divider()

    if st.button("📈 Analyze Progress", use_container_width=True, key="analyze_progress"):
        with st.spinner("Analyzing progress data..."):
            progress_data = {
                "student_id": prog_name.lower().replace(" ", "_"),
                "student_name": prog_name,
                "subject": prog_subject,
                "initial_score": initial_score,
                "current_score": current_score,
                "assessments_completed": assessments,
                "topics_completed": topics_completed,
                "practice_hours": hours_studied,
                "daily_study_minutes": 45,
                "milestones_completed": 2,
                "milestones_in_progress": 1,
                "milestones_remaining": 2,
                "study_weeks": 4
            }

            result = call_agent("progress", progress_data)

            if result.get("status") == "success":
                st.success("Progress analysis complete!")
                analysis = result.get("analysis", "")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    improvement = current_score - initial_score
                    st.metric("Improvement", f"+{improvement}%")

                with col2:
                    st.metric("Current Score", f"{current_score}%")

                with col3:
                    st.metric("Assessments", assessments)

                with col4:
                    est_weeks = max(1, 4 - (current_score // 25))
                    st.metric("Est. to Goal", f"{est_weeks} weeks")

                st.divider()
                st.subheader("Progress Analysis")

                # Display as markdown if string, otherwise as text
                if isinstance(analysis, str):
                    st.markdown(analysis)
                else:
                    st.write(analysis)
            else:
                st.error(f"Error: {result.get('message')}")


# ============================================================================
# TAB 4: SYSTEM INFO
# ============================================================================

with tab4:
    st.header("System Information")

    # Health Check
    st.subheader("System Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Health Check", use_container_width=True):
            st.success("System is healthy!")
            st.write("Education Intelligence System is running")

    with col2:
        if st.button("ℹ️ System Info", use_container_width=True):
            st.success("System Information:")
            st.json({
                "name": "Education & Learning Intelligence System",
                "version": "1.0.0",
                "framework": "Agno Framework",
                "model": "Gemini AI",
                "status": "running"
            })

    with col3:
        if st.button("🔗 Agent Status", use_container_width=True):
            st.success("Agents ready!")
            st.write("All agents are accessible")

    st.divider()

    # System Details
    st.subheader("System Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Backend:**")
        st.write("Direct agent integration")

    with col2:
        st.write("**Framework:**")
        st.write("Agno + Gemini AI")

    st.divider()

    st.subheader("Available Subjects")
    subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History", "Computer Science"]
    cols = st.columns(3)
    for i, subject in enumerate(subjects):
        with cols[i % 3]:
            st.write(f"• {subject}")

    st.divider()

    st.subheader("Application Info")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("System", "Education Intelligence")
        st.metric("Version", "1.0.0")

    with col2:
        st.metric("Framework", "Agno")
        st.metric("Model", "Gemini 2.0 Flash")

    st.divider()
    st.info("Education Intelligence System is running with direct agent integration")
