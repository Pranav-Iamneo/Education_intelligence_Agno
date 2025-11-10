"""
Education System Orchestrator - Agno Framework
Coordinates all education agents for comprehensive student analysis
"""

import logging
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.assessment_agent import assessment_agent
from agents.learning_path_agent import learning_path_agent
from agents.progress_agent import progress_agent
from agents.recommendation_agent import recommendation_agent

logger = logging.getLogger(__name__)


class EducationOrchestrator:
    """Coordinates multiple education analysis agents"""

    def __init__(self):
        """Initialize orchestrator"""
        self.assessment_agent = assessment_agent
        self.learning_path_agent = learning_path_agent
        self.progress_agent = progress_agent
        self.recommendation_agent = recommendation_agent
        logger.info("Education Orchestrator initialized")

    def assess_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate comprehensive student assessment

        Args:
            student_data: Student assessment data

        Returns:
            Complete assessment analysis
        """
        logger.info(f"Starting comprehensive assessment for: {student_data.get('student_name')}")

        try:
            logger.info("Starting assessment with Agno agents")

            assessment_result = self.assessment_agent.assess_student(student_data)

            if assessment_result.get("status") == "success":
                # Extract analysis content - handle RunOutput object
                analysis = assessment_result.get("analysis", "Assessment complete")

                # If analysis is a RunOutput object, get the content
                try:
                    if hasattr(analysis, 'content') and analysis.content:
                        analysis_text = analysis.content
                    else:
                        analysis_text = str(analysis)
                except:
                    analysis_text = str(analysis)

                accuracy = (student_data.get("correct_answers", 0) / max(student_data.get("questions_count", 1), 1)) * 100

                return {
                    "status": "success",
                    "assessment": {
                        "student_name": student_data.get("student_name"),
                        "subject": student_data.get("subject"),
                        "overall_score": accuracy,
                        "skill_level": "Intermediate",
                        "questions_answered": student_data.get("questions_count", 0),
                        "time_taken_minutes": 0,
                        "performance_by_topic": {},
                        "strengths": ["Good accuracy"],
                        "weaknesses": [],
                        "learning_path": {},
                        "progress_metrics": {},
                        "final_summary": analysis_text
                    }
                }
            else:
                return assessment_result

        except Exception as e:
            logger.error(f"Orchestration error: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Assessment failed. Please try again."
            }

    def get_progress(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get student progress analysis

        Args:
            student_data: Student progress data

        Returns:
            Progress analysis
        """
        logger.info(f"Getting progress analysis for: {student_data.get('student_name')}")

        try:
            result = self.progress_agent.analyze_progress(student_data)
            logger.info("Progress analysis completed")
            return result

        except Exception as e:
            logger.error(f"Progress analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_learning_path(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get personalized learning path

        Args:
            student_data: Student profile and assessment data

        Returns:
            Learning path recommendation
        """
        logger.info(f"Getting learning path for: {student_data.get('student_name')}")

        try:
            result = self.learning_path_agent.recommend_learning_path(student_data)
            logger.info("Learning path generated")
            return result

        except Exception as e:
            logger.error(f"Learning path error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_recommendations(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get personalized recommendations

        Args:
            student_data: Student profile and history

        Returns:
            Recommendations
        """
        logger.info(f"Getting recommendations for: {student_data.get('student_name')}")

        try:
            result = self.recommendation_agent.get_recommendations(student_data)
            logger.info("Recommendations generated")
            return result

        except Exception as e:
            logger.error(f"Recommendation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
orchestrator = EducationOrchestrator()
