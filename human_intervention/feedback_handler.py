"""
Feedback handler for human intervention in Education Intelligence System
Processes and stores human feedback on AI recommendations
"""

from datetime import datetime
from typing import Optional, Dict, Any
from utils.logger import setup_logger
from utils.database import get_db_connection, close_db_connection

logger = setup_logger(__name__)


class FeedbackHandler:
    """Handle human feedback on AI recommendations"""

    def __init__(self):
        self.logger = logger

    def submit_feedback(
        self,
        student_id: str,
        recommendation_id: str,
        feedback_type: str,
        comments: str,
        rating: Optional[int] = None
    ) -> bool:
        """
        Submit human feedback on a recommendation

        Args:
            student_id: Student identifier
            recommendation_id: Recommendation identifier
            feedback_type: Type of feedback (positive/negative/neutral)
            comments: Human feedback comments
            rating: Rating from 1-5

        Returns:
            True if feedback was stored successfully
        """
        try:
            if feedback_type not in ["positive", "negative", "neutral"]:
                self.logger.warning(f"Invalid feedback type: {feedback_type}")
                return False

            connection = get_db_connection()
            cursor = connection.cursor()

            # Create feedback table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    recommendation_id TEXT NOT NULL,
                    feedback_type TEXT NOT NULL,
                    comments TEXT,
                    rating INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Insert feedback
            cursor.execute("""
                INSERT INTO feedback (student_id, recommendation_id, feedback_type, comments, rating)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, recommendation_id, feedback_type, comments, rating))

            connection.commit()
            close_db_connection(connection)

            self.logger.info(f"Feedback stored for student {student_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error storing feedback: {e}")
            return False

    def get_feedback_history(self, student_id: str) -> list:
        """
        Get feedback history for a student

        Args:
            student_id: Student identifier

        Returns:
            List of feedback records
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT * FROM feedback WHERE student_id = ?
                ORDER BY timestamp DESC
            """, (student_id,))

            results = cursor.fetchall()
            close_db_connection(connection)

            return [dict(row) for row in results]

        except Exception as e:
            self.logger.error(f"Error retrieving feedback history: {e}")
            return []

    def get_average_rating(self, recommendation_id: str) -> Optional[float]:
        """
        Get average rating for a recommendation

        Args:
            recommendation_id: Recommendation identifier

        Returns:
            Average rating or None if no ratings exist
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT AVG(rating) as avg_rating FROM feedback
                WHERE recommendation_id = ? AND rating IS NOT NULL
            """, (recommendation_id,))

            result = cursor.fetchone()
            close_db_connection(connection)

            return result["avg_rating"] if result and result["avg_rating"] else None

        except Exception as e:
            self.logger.error(f"Error calculating average rating: {e}")
            return None
