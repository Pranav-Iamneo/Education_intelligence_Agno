"""
Data validators for Education Intelligence System
"""

from .logger import setup_logger

logger = setup_logger(__name__)


def validate_student_data(student_data: dict) -> bool:
    """
    Validate student data structure

    Args:
        student_data: Dictionary containing student information

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["student_id", "name", "email"]

    try:
        for field in required_fields:
            if field not in student_data or not student_data[field]:
                logger.warning(f"Missing required field: {field}")
                return False
        return True
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False


def validate_assessment_data(assessment_data: dict) -> bool:
    """
    Validate assessment data structure

    Args:
        assessment_data: Dictionary containing assessment information

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["student_id", "subject", "score"]

    try:
        for field in required_fields:
            if field not in assessment_data or assessment_data[field] is None:
                logger.warning(f"Missing required field: {field}")
                return False

        # Validate score is numeric and between 0-100
        score = assessment_data["score"]
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            logger.warning(f"Invalid score: {score}")
            return False

        return True
    except Exception as e:
        logger.error(f"Assessment validation error: {e}")
        return False
