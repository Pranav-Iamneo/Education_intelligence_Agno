EDUCATION & LEARNING INTELLIGENCE SYSTEM
==========================================

PROBLEM STATEMENT
=================

The Education & Learning Intelligence System is an AI-powered educational platform designed to
provide comprehensive student assessment, personalized learning path generation, progress tracking,
and intelligent learning recommendations. The system aims to bridge the gap between traditional
educational approaches and personalized, adaptive learning experiences by leveraging artificial
intelligence and human oversight.

KEY OBJECTIVES:
- Assess student knowledge and accurately identify current skill levels
- Generate personalized, adaptive learning paths tailored to individual student needs
- Track and analyze student progress over time with detailed metrics
- Provide AI-driven intelligent recommendations for learning resources and next steps
- Enable human intervention through approval workflows and feedback mechanisms for continuous improvement


FILE STRUCTURE AND PURPOSE
===========================

education-intelligence/
├── agents/                          Core AI agents directory
│   ├── __init__.py                  Package initialization
│   ├── assessment_agent.py          Student knowledge assessment and analysis
│   ├── learning_path_agent.py       Personalized learning path generation
│   ├── progress_agent.py            Learning progress tracking and analysis
│   ├── recommendation_agent.py      AI-driven learning recommendations
│   └── orchestrator.py              Coordinates all agents and workflows
│
├── human_intervention/              Human oversight and feedback management
│   ├── __init__.py                  Package initialization
│   ├── approval_manager.py          Manages approval workflows for decisions
│   └── feedback_handler.py          Collects and processes human feedback
│
├── utils/                           Utility and helper modules
│   ├── __init__.py                  Package initialization
│   ├── database.py                  SQLite database operations
│   ├── logger.py                    Logging configuration and setup
│   └── validators.py                Data validation functions
│
├── config.py                        Configuration settings and environment variables
├── main.py                          Application entry point with CLI, Streamlit, API modes
├── streamlit_ui.py                  Web interface using Streamlit framework
├── tests.py                         Test suite with pytest framework
├── .env                             Environment variables (API keys, database config)
└── education.db                     SQLite database file


AGENTS AND THEIR IMPORTANT METHODS
===================================

ORCHESTRATOR (agents/orchestrator.py)
-------------------------------------

Class: EducationOrchestrator
Purpose: Coordinates all AI agents for comprehensive student analysis and recommendations

Method: __init__()
Parameters: None
Returns: Initializes instance with all four specialized agents

Method: assess_student(student_data: Dict[str, Any])
Parameters:
  - student_data: Dictionary containing student information and assessment results
    Required fields: student_id, name, email, subject, difficulty_level, questions_count,
                     correct_answers, incorrect_answers, partial_answers
Returns: Dictionary with comprehensive assessment results including skill level and feedback

Method: get_progress(student_data: Dict[str, Any])
Parameters:
  - student_data: Dictionary containing student history and metrics
    Required fields: student_id, name, subject, assessment_history, learning_activities,
                     milestones_status
Returns: Dictionary with progress analysis, trends, and improvement metrics

Method: get_learning_path(student_data: Dict[str, Any])
Parameters:
  - student_data: Dictionary containing student profile and learning preferences
    Required fields: student_id, current_skill_level, target_level, learning_style,
                     available_hours_per_week, weak_areas, strong_areas
Returns: Dictionary with topic sequence, timeline, resources, and milestones

Method: get_recommendations(student_data: Dict[str, Any])
Parameters:
  - student_data: Dictionary with student profile and learning context
    Required fields: student_id, skill_level, learning_style, weak_areas, strong_areas,
                     career_interests, available_time
Returns: Dictionary with recommended topics, resources, study techniques, and career alignment


ASSESSMENT AGENT (agents/assessment_agent.py)
----------------------------------------------

Class: AssessmentAgent extends Agent
Purpose: Evaluates student knowledge, identifies skill levels, and detects misconceptions
AI Model: Gemini 2.0-flash (via Agno framework)
Database: SQLite with Agno integration

Method: assess_student(student_data: Dict[str, Any])
Parameters:
  - student_data: Assessment information dictionary with:
    - student_name (string): Name of the student
    - subject (string): Subject being assessed
    - difficulty_level (string): Level of assessment difficulty
    - question_count (integer): Total number of questions
    - correct_count (integer): Number of correct answers
    - incorrect_count (integer): Number of incorrect answers
    - partial_count (integer): Number of partially correct answers
Returns: Dictionary containing:
  - overall_accuracy (string): Percentage of correct answers
  - skill_level (string): Beginner, Intermediate, or Advanced
  - performance_by_topic (dictionary): Score breakdown for each topic
  - strengths (list): Identified knowledge strengths
  - weaknesses (list): Identified knowledge gaps
  - confidence_scores (dictionary): Confidence level per topic
  - misconceptions_detected (list): Specific conceptual errors found
  - actionable_feedback (string): Specific guidance for improvement
  - comprehensive_summary (string): Overall assessment narrative


LEARNING PATH AGENT (agents/learning_path_agent.py)
----------------------------------------------------

Class: LearningPathAgent extends Agent
Purpose: Designs custom, personalized learning routes for each student
AI Model: Gemini 2.0-flash (via Agno framework)

Method: recommend_learning_path(student_data: Dict[str, Any])
Parameters:
  - student_data: Student profile dictionary with:
    - student_name (string): Name of the student
    - current_skill_level (string): Beginner, Intermediate, or Advanced
    - target_level (string): Desired skill level to achieve
    - learning_style (string): Visual, Auditory, Reading, Kinesthetic
    - available_hours_per_week (integer): Weekly study commitment
    - weak_areas (list): Topics needing improvement
    - strong_areas (list): Topics with mastery
Returns: Dictionary containing:
  - recommended_topic_sequence (list): Topics in learning order from foundational to advanced
  - estimated_completion_timeline (string): Timeline to achieve target level
  - daily_study_schedule (string): Recommended daily study hours and structure
  - resource_recommendations (dictionary): Videos, textbooks, tools, projects
  - weekly_milestones (list): Checkpoint goals for each week
  - practice_problems (list): Exercises for skill development
  - difficulty_progression_strategy (string): How difficulty should increase
  - topic_integration_opportunities (list): Cross-subject connections
  - review_and_reinforcement_schedule (string): Spaced repetition plan
  - learning_path_narrative (string): Comprehensive pathway description


PROGRESS AGENT (agents/progress_agent.py)
------------------------------------------

Class: ProgressAgent extends Agent
Purpose: Monitors and analyzes student learning progress over time with trend analysis
AI Model: Gemini 2.0-flash (via Agno framework)

Method: analyze_progress(student_data: Dict[str, Any])
Parameters:
  - student_data: Student progress data dictionary with:
    - student_name (string): Name of the student
    - subject (string): Subject being tracked
    - assessment_history (list): Previous assessment results with dates and scores
    - learning_activity_metrics (dictionary): Hours spent, resources used, practice completed
    - milestone_status (dictionary): Completion status of key milestones
    - historical_data (list): Long-term learning records
Returns: Dictionary containing:
  - overall_progress_score (string): Percentage of goal achievement
  - progress_summary (string): High-level overview of progress
  - improvement_rate (string): Percentage improvement per week or month
  - trajectory_analysis (string): Current learning velocity and direction
  - performance_by_topic (dictionary): Progress in each topic area
  - achieved_strengths (list): Topics where progress is strong
  - areas_needing_work (list): Topics requiring more focus
  - progress_trends (string): Accelerating, steady, plateauing, or declining
  - detected_learning_patterns (dictionary): Identified study habits and patterns
  - milestone_achievement_analysis (string): Status of key checkpoints
  - estimated_time_to_goal (string): Projected completion date
  - optimization_recommendations (list): Targeted improvement suggestions
  - motivational_assessment (string): Encouragement and recognition


RECOMMENDATION AGENT (agents/recommendation_agent.py)
-----------------------------------------------------

Class: RecommendationAgent extends Agent
Purpose: Provides AI-driven learning recommendations and personalized suggestions
AI Model: Gemini 2.0-flash (via Agno framework)

Method: get_recommendations(student_data: Dict[str, Any])
Parameters:
  - student_data: Student profile dictionary with:
    - student_name (string): Name of the student
    - current_skill_level (string): Current competency level
    - learning_style (string): Preferred learning mode
    - weak_areas (list): Topics needing improvement
    - strong_areas (list): Topics with mastery
    - career_interests (string): Professional goals
    - available_time (integer): Weekly hours available for learning
Returns: Dictionary containing:
  - next_topic_recommendation (string): Recommended topic with justification
  - importance_explanation (string): Why this topic matters
  - prerequisites_check (string): Assessment of prerequisite knowledge
  - recommended_study_techniques (dictionary): Multiple proven approaches
  - resource_recommendations (dictionary): Videos, books, tools, podcasts
  - similar_content (list): Alternative resources on the same topic
  - study_group_recommendations (list): Peer learning opportunities
  - tool_recommendations (dictionary): Software and platform suggestions
  - career_path_alignment (string): Relevance to professional goals
  - success_factors (list): Key elements for successful learning
  - challenges_to_expect (list): Potential difficulties and obstacles
  - timeline_and_milestones (string): Completion estimate with checkpoints
  - motivational_message (string): Personalized encouragement


APPROVAL MANAGER (human_intervention/approval_manager.py)
----------------------------------------------------------

Class: ApprovalManager
Purpose: Manage approval workflows for critical AI decisions with status tracking

Method: create_approval_request(student_id: str, decision_type: str, decision_data: Dict[str, Any], priority: str)
Parameters:
  - student_id (string): Identifier for the student
  - decision_type (string): Type of decision requiring approval
  - decision_data (dictionary): Data supporting the decision
  - priority (string): Request priority level, default is "normal"
Returns: String containing the approval request ID or None if creation failed

Method: approve_request(request_id: str, reviewer_id: str, comments: str)
Parameters:
  - request_id (string): ID of the approval request
  - reviewer_id (string): ID of the reviewer approving the request
  - comments (string): Optional review comments
Returns: Boolean indicating success or failure

Method: reject_request(request_id: str, reviewer_id: str, comments: str)
Parameters:
  - request_id (string): ID of the approval request
  - reviewer_id (string): ID of the reviewer rejecting the request
  - comments (string): Reason for rejection
Returns: Boolean indicating success or failure

Method: request_revision(request_id: str, reviewer_id: str, comments: str)
Parameters:
  - request_id (string): ID of the approval request
  - reviewer_id (string): ID of the reviewer requesting revision
  - comments (string): Specific revision suggestions
Returns: Boolean indicating success or failure

Method: get_pending_requests(priority: str optional)
Parameters:
  - priority (string): Optional filter for request priority level
Returns: List of dictionaries containing pending approval requests

Method: get_request_status(request_id: str)
Parameters:
  - request_id (string): ID of the specific approval request
Returns: Dictionary with request status and details or None if not found

Approval Status Values: PENDING, APPROVED, REJECTED, NEEDS_REVISION


FEEDBACK HANDLER (human_intervention/feedback_handler.py)
----------------------------------------------------------

Class: FeedbackHandler
Purpose: Handle and manage human feedback on AI recommendations for continuous improvement

Method: submit_feedback(student_id: str, recommendation_id: str, feedback_type: str, comments: str, rating: int optional)
Parameters:
  - student_id (string): Identifier for the student
  - recommendation_id (string): ID of the recommendation being rated
  - feedback_type (string): Type of feedback - "positive", "negative", or "neutral"
  - comments (string): Detailed feedback comments
  - rating (integer): Optional 1-5 scale rating
Returns: Boolean indicating successful submission

Method: get_feedback_history(student_id: str)
Parameters:
  - student_id (string): Identifier for the student
Returns: List of dictionaries containing all feedback records for the student

Method: get_average_rating(recommendation_id: str)
Parameters:
  - recommendation_id (string): ID of the recommendation
Returns: Float representing average rating or None if no ratings exist


UTILITY FUNCTIONS AND VALIDATORS
=================================

DATABASE UTILITIES (utils/database.py)
--------------------------------------

Function: get_db_connection()
Parameters: None
Returns: sqlite3.Connection object for database access

Function: close_db_connection(connection: sqlite3.Connection)
Parameters:
  - connection (sqlite3.Connection): Database connection to close
Returns: None

Function: execute_query(query: str, params: tuple optional)
Parameters:
  - query (string): SQL query to execute
  - params (tuple): Optional parameters for parameterized queries
Returns: Result from query execution


LOGGER SETUP (utils/logger.py)
------------------------------

Function: setup_logger(name: str optional)
Parameters:
  - name (string): Optional name for the logger
Returns: logging.Logger object configured with console handler and formatting


VALIDATORS (utils/validators.py)
--------------------------------

Function: validate_student_data(student_data: dict)
Parameters:
  - student_data (dictionary): Student information to validate
Returns: Boolean indicating validity
Checks: Required fields student_id, name, email presence

Function: validate_assessment_data(assessment_data: dict)
Parameters:
  - assessment_data (dictionary): Assessment information to validate
Returns: Boolean indicating validity
Checks: Required fields and score range validation (0-100)


CONFIGURATION (config.py)
-------------------------

Class: Settings
Contains application configuration with the following attributes:
  - GEMINI_API_KEY (string): API key for Google Gemini service
  - AGENT_MODEL (string): AI model name "gemini-2.0-flash"
  - API_PORT (integer): Server port, default 8083
  - API_HOST (string): Server host, default "localhost"
  - DB_FILE (string): Database file path, default "education.db"
  - DEBUG (boolean): Debug mode flag
  - LOG_LEVEL (string): Logging level, default "INFO"
  - APP_NAME (string): Application name
  - APP_VERSION (string): Version number "1.0.0"
  - DESCRIPTION (string): Application description


RUNNING COMMANDS
================

STREAMLIT WEB INTERFACE (Default Mode)
---------------------------------------

Command: python3 -m streamlit run main.py
Alternative: python3 main.py
Description: Launches interactive web dashboard
Access Point: http://localhost:8501
Features:
  - Tabbed interface for Assessment, Learning Paths, Progress, Recommendations
  - Real-time AI analysis and recommendations
  - Interactive student profile management
  - Visual data presentation
Requirements: Streamlit installation with "pip install streamlit"


API SERVER MODE
---------------

Command: python3 main.py --api
Description: Starts FastAPI/Uvicorn REST API server
Access Point: http://localhost:8083
Endpoints:
  - POST /assess - Student assessment
  - POST /learning-path - Generate learning path
  - POST /progress - Analyze progress
  - POST /recommendations - Get recommendations
  - POST /approval - Create approval request
Requirements: uvicorn and fastapi with "pip install uvicorn fastapi"


COMMAND-LINE INTERFACE MODE
----------------------------

Command: python3 main.py --cli
Description: Interactive CLI with text-based prompts
Features:
  - Student ID entry
  - Operation selection menu
  - Text-based output display
  - Sequential workflow execution
Interface: Text-based prompts and responses


ADDITIONAL COMMAND OPTIONS
---------------------------

Command: python3 main.py --version
Description: Display application version

Command: python3 main.py -v
Description: Enable verbose logging output

Command: python3 main.py --help
Description: Show command help and usage information

Command: python3 -m pytest tests.py -v
Description: Run test suite with verbose output
Function: Executes all unit and integration tests


ENVIRONMENT SETUP
-----------------

Configuration file: .env
Required entries:
  GEMINI_API_KEY=your_api_key_here
  API_PORT=8083
  API_HOST=localhost
  DATABASE=education.db
  DEBUG=False
  LOG_LEVEL=INFO


EXPECTED OUTPUT
===============

ASSESSMENT AGENT OUTPUT
-----------------------

Assessment results include:
  Overall accuracy percentage: 85%
  Skill level: Intermediate
  Performance by topic:
    - Topic A: 90%
    - Topic B: 75%
    - Topic C: 85%
  Identified strengths:
    - Strong conceptual understanding
    - Excellent problem-solving skills
  Identified weaknesses:
    - Difficulty with advanced applications
    - Need reinforcement in specific area
  Confidence scores:
    - High confidence: 80%
    - Medium confidence: 70%
  Misconceptions detected:
    - Common error type 1
    - Conceptual gap in area 2
  Actionable feedback:
    - Recommendation 1 for improvement
    - Recommendation 2 for growth
  Overall summary:
    Comprehensive assessment narrative describing current understanding level


LEARNING PATH OUTPUT
--------------------

Learning path generation includes:
  Topic Sequence:
    Week 1-2: Foundational concepts
    Week 3-4: Core principles
    Week 5-6: Advanced applications
    Week 7-8: Integration projects
  Timeline: 8 weeks estimated completion
  Daily Schedule: 2 hours per day recommended
  Resources:
    Videos:
      - Course on Platform A
      - Tutorial series on Platform B
    Books:
      - Textbook Title 1
      - Reference Guide Title 2
    Interactive Tools:
      - Practice platform name
      - Simulation software
    Projects:
      - Real-world application project 1
      - Capstone project
  Milestones:
    - Week 2: Complete foundational assessment
    - Week 4: Demonstrate core knowledge
    - Week 6: Apply advanced concepts
    - Week 8: Final comprehensive project
  Success Checklist:
    - Foundational quiz passed
    - Core assessment completed
    - Project deliverables submitted


PROGRESS ANALYSIS OUTPUT
------------------------

Progress tracking includes:
  Overall Progress Score: 75%
  Progress Summary: Student on track with consistent improvement
  Improvement Rate: Plus 5 percent per week
  Trajectory Analysis: Steady upward trend with accelerating pace
  Topic Breakdown:
    - Topic A Progress: 85 percent
    - Topic B Progress: 70 percent
    - Topic C Progress: 80 percent
  Achieved Improvements:
    - Week 2 improvement in Topic A
    - Week 4 breakthrough in Topic B
  Areas Needing Work:
    - Topic C requires targeted practice
    - Advanced applications need focus
  Progress Trends: Accelerating
  Detected Learning Patterns:
    - Peak performance in morning sessions
    - Better retention with hands-on practice
  Milestone Achievement:
    - Completed: Foundation assessment
    - In Progress: Core concepts
    - Pending: Advanced applications
  Estimated Time to Goal: 3 weeks remaining
  Optimization Recommendations:
    - Increase practice frequency
    - Add peer study sessions
    - Utilize interactive tools more


RECOMMENDATIONS OUTPUT
----------------------

Personalized recommendations include:
  Next Topic Recommendation:
    Advanced Data Structures with clear justification
  Importance Explanation:
    Essential for interview preparation and system design
  Prerequisites Check:
    All prerequisites met with strong foundation
  Recommended Study Techniques:
    Primary Approach: Active recall with practice problems
    Alternative Approach 1: Teaching method explanation
    Alternative Approach 2: Visual diagram mapping
  Resource Recommendations:
    Videos:
      - LeetCode Video Series on Data Structures
      - MIT OpenCourseWare Lecture
    Books:
      - Introduction to Algorithms by Cormen
      - Cracking the Coding Interview
    Tools:
      - LeetCode platform
      - CodeSignal practice platform
    Podcasts:
      - Software Engineering Daily
      - CoRecursive Podcast
  Similar and Alternative Content:
    - Alternative book with different approach
    - Different course with supplementary content
  Study Group Recommendations:
    - College prep study group meets Tuesdays
    - Online community forum for peer discussion
  Tool Recommendations:
    - Visualization: Algorithm Visualizer Website
    - Productivity: Focus Timer Application
    - Forums: Stack Overflow community
  Career Path Alignment:
    - Directly relevant to software engineering roles
    - Essential for internship interview success
    - Core skill for data-focused positions
  Success Factors:
    - Consistent daily practice is crucial
    - Focus on understanding not just memorization
    - Apply concepts to real problems
  Challenges to Expect:
    - Complex topics may require multiple exposures
    - Time complexity analysis can be challenging
    - Pattern recognition takes practice
  Timeline and Milestones:
    - Week 1: Understand basic data structure concepts
    - Week 2: Implement common structures
    - Week 3: Optimize algorithms
    - Week 4: Interview problem solving
    - Estimated Completion: 4 weeks
  Motivational Message:
    You have demonstrated strong capability in foundational concepts
    This next step will significantly enhance your technical career prospects


DATABASE SCHEMA
===============

Approval Requests Table:

CREATE TABLE approval_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    decision_data TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    priority TEXT DEFAULT 'normal',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME,
    reviewer_id TEXT,
    reviewer_comments TEXT
)

Feedback Table:

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    recommendation_id TEXT NOT NULL,
    feedback_type TEXT NOT NULL,
    comments TEXT,
    rating INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)


TECHNOLOGY STACK
================

Framework: Agno - AI agent framework for building intelligent systems
AI Model: Google Gemini 2.0-flash - State-of-the-art language model
Web UI: Streamlit - Open-source app framework for data applications
API: FastAPI with Uvicorn - Modern Python web framework for APIs
Database: SQLite - Lightweight, file-based relational database
Language: Python 3.x - Primary programming language
Testing: pytest - Testing framework for Python applications
Logging: Python logging module - Built-in logging infrastructure


KEY WORKFLOWS AND PROCESSES
============================

STUDENT ASSESSMENT WORKFLOW
---------------------------

Step 1: Data Collection
  - User enters student identification information
  - User provides assessment results and quiz responses

Step 2: AI Analysis
  - Assessment Agent processes student performance data
  - AI model analyzes knowledge patterns and identifies gaps

Step 3: Results Generation
  - System calculates overall accuracy and skill level
  - AI identifies topic-specific performance and misconceptions

Step 4: Output and Storage
  - Results displayed to user with detailed feedback
  - Assessment data stored in database for future reference

Step 5: Human Review Option
  - Critical findings can be submitted for human approval
  - Educators can review and provide feedback


LEARNING PATH GENERATION WORKFLOW
----------------------------------

Step 1: Profile Analysis
  - Orchestrator receives student profile and assessment results
  - System analyzes current skill level and target goals

Step 2: Path Design
  - Learning Path Agent creates customized curriculum sequence
  - AI determines optimal topic ordering and pacing

Step 3: Resource Compilation
  - System identifies high-quality learning resources
  - Milestones and checkpoints established

Step 4: Timeline Development
  - Realistic completion timeline calculated
  - Daily and weekly study schedules generated

Step 5: Approval and Implementation
  - Learning path can be submitted for educator approval
  - Approved path provided to student with detailed guidance


PROGRESS TRACKING WORKFLOW
--------------------------

Step 1: Data Aggregation
  - Progress Agent retrieves historical assessment data
  - System compiles learning activity metrics

Step 2: Analysis
  - AI analyzes improvement trends over time
  - System identifies learning patterns and plateaus

Step 3: Performance Evaluation
  - Topic-by-topic progress calculated
  - Milestone achievement assessed

Step 4: Insight Generation
  - AI identifies areas of concern or breakthrough
  - Optimization recommendations created

Step 5: Communication
  - Progress report generated for student
  - Motivation and guidance provided based on trajectory


RECOMMENDATION WORKFLOW
-----------------------

Step 1: Context Analysis
  - Recommendation Agent analyzes student profile
  - System reviews learning history and preferences

Step 2: Topic Evaluation
  - Next logical topic selected based on progress
  - Prerequisites verified and importance assessed

Step 3: Resource Selection
  - High-quality resources identified for topic
  - Multiple learning techniques recommended

Step 4: Career Alignment
  - Recommendations aligned with student goals
  - Success factors identified

Step 5: Feedback Collection
  - Students provide ratings on recommendations
  - Human feedback used to improve future suggestions


TESTING AND QUALITY ASSURANCE
==============================

Test Suite Location: tests.py

Test Coverage Areas:
  - Student data validation with valid and invalid inputs
  - Assessment data validation with score range checks
  - Database connection and query execution
  - Approval manager workflow and status tracking
  - Feedback handler submission and retrieval
  - Logger configuration and output formatting
  - Agent functionality with mocked responses
  - Integration testing between components

Running Tests:

Command: python3 -m pytest tests.py -v
Description: Executes complete test suite with verbose output
Output: Detailed test results for each test case

Command: python3 -m pytest tests.py -k assessment_agent
Description: Run only tests containing "assessment_agent" in name
Output: Subset of tests matching criteria

Expected Test Results:
  - All validation tests pass
  - Database operations succeed
  - Approval workflow executes correctly
  - Feedback submission and retrieval work
  - Logger configured properly
  - Agent mocks return expected outputs


DEPLOYMENT CONSIDERATIONS
=========================

Requirements:
  - Python 3.8 or higher
  - Required packages: agno, google-generativeai, streamlit, fastapi, uvicorn, pytest
  - Valid Google Gemini API key
  - Sufficient disk space for SQLite database

Configuration Steps:
  1. Create .env file with required variables
  2. Set GEMINI_API_KEY environment variable
  3. Install dependencies with pip install -r requirements.txt
  4. Initialize database with schema setup script
  5. Run application with chosen mode

Performance Considerations:
  - Database indexing on student_id for faster queries
  - API rate limiting for Gemini service
  - Caching for frequently accessed student data
  - Async processing for long-running analysis tasks

Security Considerations:
  - Secure API key management in .env file
  - Input validation for all user data
  - SQL injection prevention through parameterized queries
  - Role-based access control for approval workflows
  - Data encryption for sensitive student information


TROUBLESHOOTING
===============

Common Issues and Solutions:

Issue: GEMINI_API_KEY not found
Solution: Ensure .env file exists and contains valid API key

Issue: Port 8501 or 8083 already in use
Solution: Modify API_PORT in config.py or kill process using port

Issue: Database connection errors
Solution: Check DATABASE path in .env and verify file exists and permissions

Issue: Agent responses timeout
Solution: Increase timeout values or check API rate limits

Issue: Streamlit not displaying
Solution: Verify streamlit installation and try clearing cache


END OF PROBLEM DESCRIPTION
==========================
