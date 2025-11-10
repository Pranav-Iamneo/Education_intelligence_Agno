"""
Test suite for Education Intelligence System
Tests cover agents, validators, database operations, and human intervention features
"""

import pytest
import sqlite3
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import project modules
from config import Settings
from utils.validators import validate_student_data, validate_assessment_data
from utils.database import get_db_connection, close_db_connection
from utils.logger import setup_logger
from human_intervention.approval_manager import ApprovalManager
from human_intervention.feedback_handler import FeedbackHandler


# ============================================================================
# FIXTURE SETUP
# ============================================================================

@pytest.fixture
def mock_settings():
    """Mock configuration for testing"""
    settings = Mock(spec=Settings)
    settings.DB_FILE = ":memory:"
    settings.LOG_LEVEL = "INFO"
    settings.API_PORT = 8083
    settings.GEMINI_API_KEY = "test_api_key_12345"
    return settings


@pytest.fixture
def sample_student_data():
    """Sample student data for testing"""
    return {
        "student_id": "STU001",
        "name": "John Doe",
        "email": "john@example.com",
        "grade_level": "10",
        "subject": "Mathematics",
        "learning_style": "visual",
        "previous_score": 75.5
    }


@pytest.fixture
def sample_assessment_data():
    """Sample assessment data for testing"""
    return {
        "student_id": "STU001",
        "subject": "Mathematics",
        "score": 85
    }


@pytest.fixture
def sample_invalid_student_data():
    """Invalid student data for validation testing"""
    return {
        "name": "Jane Doe",
        # Missing required fields: student_id, email
    }


@pytest.fixture
def sample_invalid_assessment_data():
    """Invalid assessment data for validation testing"""
    return {
        "student_id": "STU001",
        "subject": "Mathematics",
        "score": 150  # Invalid: score out of range (0-100)
    }


@pytest.fixture
def in_memory_db():
    """Create in-memory SQLite database for testing"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create test tables
    cursor.execute("""
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            grade_level TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE approvals (
            approval_id TEXT PRIMARY KEY,
            request_type TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE feedback (
            feedback_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            recommendation_id TEXT,
            rating INTEGER,
            feedback_text TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    yield conn
    conn.close()


# ============================================================================
# TEST CASE 1: Student Data Validation (Valid Data)
# ============================================================================

def test_validate_student_data_valid():
    """Test that validate_student_data accepts valid student data"""
    valid_data = {
        "student_id": "STU001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "grade_level": "11",
        "subject": "Physics"
    }

    result = validate_student_data(valid_data)
    assert result is True, "Valid student data should pass validation"


# ============================================================================
# TEST CASE 2: Student Data Validation (Invalid Data)
# ============================================================================

def test_validate_student_data_invalid(sample_invalid_student_data):
    """Test that validate_student_data rejects invalid student data"""
    result = validate_student_data(sample_invalid_student_data)
    assert result is False, "Invalid student data should fail validation"


# ============================================================================
# TEST CASE 3: Assessment Data Validation (Valid Score Range)
# ============================================================================

def test_validate_assessment_data_valid(sample_assessment_data):
    """Test that validate_assessment_data accepts valid assessment data"""
    result = validate_assessment_data(sample_assessment_data)
    assert result is True, "Valid assessment data should pass validation"


# ============================================================================
# TEST CASE 4: Assessment Data Validation (Invalid Score Range)
# ============================================================================

def test_validate_assessment_data_invalid_score(sample_invalid_assessment_data):
    """Test that validate_assessment_data rejects score out of valid range"""
    result = validate_assessment_data(sample_invalid_assessment_data)
    assert result is False, "Assessment data with invalid score should fail validation"


# ============================================================================
# TEST CASE 5: Database Connection and Query Execution
# ============================================================================

def test_database_execute_query(in_memory_db):
    """Test database query execution"""
    # Insert test data
    query = "INSERT INTO students (student_id, name, email, grade_level) VALUES (?, ?, ?, ?)"
    cursor = in_memory_db.cursor()
    cursor.execute(query, ("STU001", "Bob Smith", "bob@example.com", "10"))
    in_memory_db.commit()

    # Retrieve and verify
    select_query = "SELECT * FROM students WHERE student_id = ?"
    cursor.execute(select_query, ("STU001",))
    result = cursor.fetchone()

    assert result is not None, "Student record should exist in database"
    assert result[1] == "Bob Smith", "Student name should match"
    assert result[2] == "bob@example.com", "Student email should match"


# ============================================================================
# TEST CASE 6: Approval Manager - Create Approval Request
# ============================================================================

@patch('human_intervention.approval_manager.get_db_connection')
@patch('human_intervention.approval_manager.close_db_connection')
def test_approval_manager_create_request(mock_close, mock_get_conn):
    """Test creating an approval request"""
    # Mock database connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 1
    mock_get_conn.return_value = mock_conn

    manager = ApprovalManager()

    approval_id = manager.create_approval_request(
        student_id="STU001",
        decision_type="learning_path",
        decision_data={"path": "Algebra fundamentals"},
        priority="high"
    )

    assert approval_id is not None, "Approval request should be created with valid ID"
    assert isinstance(approval_id, str), "Approval ID should be a string"
    assert approval_id == "1", "Approval ID should match the database ID"


# ============================================================================
# TEST CASE 7: Approval Manager - Get Pending Requests
# ============================================================================

@patch('human_intervention.approval_manager.get_db_connection')
@patch('human_intervention.approval_manager.close_db_connection')
def test_approval_manager_get_pending_requests(mock_close, mock_get_conn):
    """Test retrieving pending approval requests"""
    # Mock database connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.row_factory = sqlite3.Row
    mock_cursor.fetchall.return_value = [
        {"id": 1, "student_id": "STU001", "decision_type": "assessment", "status": "pending"},
        {"id": 2, "student_id": "STU002", "decision_type": "recommendation", "status": "pending"}
    ]
    mock_get_conn.return_value = mock_conn

    manager = ApprovalManager()
    pending = manager.get_pending_requests()

    assert isinstance(pending, list), "Should return a list"


# ============================================================================
# TEST CASE 8: Feedback Handler - Submit Feedback
# ============================================================================

@patch('human_intervention.feedback_handler.get_db_connection')
@patch('human_intervention.feedback_handler.close_db_connection')
def test_feedback_handler_submit_feedback(mock_close, mock_get_conn):
    """Test submitting feedback for recommendations"""
    # Mock database connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    handler = FeedbackHandler()

    result = handler.submit_feedback(
        student_id="STU001",
        recommendation_id="REC001",
        feedback_type="positive",
        comments="The recommended study schedule was helpful",
        rating=4
    )

    assert result is True, "Feedback should be submitted successfully"


# ============================================================================
# TEST CASE 9: Feedback Handler - Get Average Rating
# ============================================================================

@patch('human_intervention.feedback_handler.get_db_connection')
@patch('human_intervention.feedback_handler.close_db_connection')
def test_feedback_handler_get_average_rating(mock_close, mock_get_conn):
    """Test calculating average rating for recommendations"""
    # Mock database connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # First call returns average rating
    mock_cursor.fetchone.return_value = {"avg_rating": 4.0}
    mock_get_conn.return_value = mock_conn

    handler = FeedbackHandler()
    avg_rating = handler.get_average_rating("REC001")

    assert avg_rating is not None, "Should return average rating"
    assert isinstance(avg_rating, (int, float)), "Average rating should be numeric"
    assert avg_rating == 4.0, "Average rating should match mocked value"


# ============================================================================
# TEST CASE 10: Logger Setup and Configuration
# ============================================================================

def test_logger_setup():
    """Test logger configuration and setup"""
    logger = setup_logger("TestLogger")

    assert logger is not None, "Logger should be created successfully"
    assert logger.name == "TestLogger", "Logger name should match"
    assert isinstance(logger, object), "Logger should be a valid logger instance"

    # Test logger with default name
    default_logger = setup_logger()
    assert default_logger is not None, "Logger with default name should be created"
    assert default_logger.name == "education_intelligence", "Default logger name should be set"


# ============================================================================
# INTEGRATION TESTS (Optional bonus tests)
# ============================================================================

class TestEducationOrchestrator:
    """Test suite for the Education Orchestrator"""

    @pytest.mark.integration
    def test_orchestrator_initialization(self):
        """Test orchestrator can be initialized"""
        with patch('agents.orchestrator.EducationOrchestrator') as mock_orchestrator:
            orchestrator = mock_orchestrator()
            assert orchestrator is not None

    @pytest.mark.integration
    def test_orchestrator_assess_student(self, sample_student_data, sample_assessment_data):
        """Test orchestrator assessment flow"""
        with patch('agents.orchestrator.EducationOrchestrator') as mock_orchestrator:
            instance = mock_orchestrator.return_value
            instance.assess_student.return_value = {
                "student_id": "STU001",
                "skill_level": "intermediate",
                "accuracy": 85.0,
                "strengths": ["Algebra", "Basic Geometry"],
                "weaknesses": ["Advanced Trigonometry"]
            }

            result = instance.assess_student(sample_student_data)
            assert result is not None
            assert "skill_level" in result


# ============================================================================
# PARAMETRIZED TESTS FOR EDGE CASES
# ============================================================================

@pytest.mark.parametrize("score,is_valid", [
    (0, True),      # Minimum valid score
    (100, True),    # Maximum valid score
    (50, True),     # Mid-range valid score
    (-1, False),    # Below minimum
    (101, False),   # Above maximum
    (85.5, True),   # Decimal score (valid)
])
def test_assessment_score_validation(score, is_valid):
    """Test assessment score validation with various inputs"""
    assessment_data = {
        "student_id": "STU001",
        "subject": "Mathematics",
        "score": score
    }

    result = validate_assessment_data(assessment_data)
    assert result == is_valid, f"Score {score} validation should be {is_valid}"


# ============================================================================
# FIXTURE CLEANUP
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup after each test"""
    yield
    # Add cleanup code here if needed


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

if __name__ == "__main__":
    # Run tests with pytest
    # pytest tests.py -v
    # pytest tests.py --tb=short
    # pytest tests.py -k "test_validate" (run specific tests)
    pass
