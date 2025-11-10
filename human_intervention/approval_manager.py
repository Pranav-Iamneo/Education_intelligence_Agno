"""
Approval manager for human intervention in Education Intelligence System
Handles approval workflows for critical AI decisions
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from utils.logger import setup_logger
from utils.database import get_db_connection, close_db_connection

logger = setup_logger(__name__)


class ApprovalStatus(Enum):
    """Approval status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


class ApprovalManager:
    """Manage approval workflows for critical decisions"""

    def __init__(self):
        self.logger = logger

    def create_approval_request(
        self,
        student_id: str,
        decision_type: str,
        decision_data: Dict[str, Any],
        priority: str = "normal"
    ) -> Optional[str]:
        """
        Create an approval request for a critical decision

        Args:
            student_id: Student identifier
            decision_type: Type of decision (learning_path/curriculum/dismissal)
            decision_data: Detailed decision data
            priority: Priority level (low/normal/high)

        Returns:
            Approval request ID or None if failed
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Create approval requests table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS approval_requests (
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
            """)

            # Insert approval request
            import json
            cursor.execute("""
                INSERT INTO approval_requests
                (student_id, decision_type, decision_data, status, priority)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, decision_type, json.dumps(decision_data), "pending", priority))

            connection.commit()
            request_id = cursor.lastrowid
            close_db_connection(connection)

            self.logger.info(f"Approval request {request_id} created for student {student_id}")
            return str(request_id)

        except Exception as e:
            self.logger.error(f"Error creating approval request: {e}")
            return None

    def approve_request(
        self,
        request_id: str,
        reviewer_id: str,
        comments: str = ""
    ) -> bool:
        """
        Approve an approval request

        Args:
            request_id: Approval request ID
            reviewer_id: ID of the reviewer
            comments: Reviewer comments

        Returns:
            True if approval was successful
        """
        return self._update_approval_status(
            request_id,
            ApprovalStatus.APPROVED.value,
            reviewer_id,
            comments
        )

    def reject_request(
        self,
        request_id: str,
        reviewer_id: str,
        comments: str
    ) -> bool:
        """
        Reject an approval request

        Args:
            request_id: Approval request ID
            reviewer_id: ID of the reviewer
            comments: Rejection comments

        Returns:
            True if rejection was successful
        """
        return self._update_approval_status(
            request_id,
            ApprovalStatus.REJECTED.value,
            reviewer_id,
            comments
        )

    def request_revision(
        self,
        request_id: str,
        reviewer_id: str,
        comments: str
    ) -> bool:
        """
        Request revision for an approval request

        Args:
            request_id: Approval request ID
            reviewer_id: ID of the reviewer
            comments: Revision comments

        Returns:
            True if revision request was successful
        """
        return self._update_approval_status(
            request_id,
            ApprovalStatus.NEEDS_REVISION.value,
            reviewer_id,
            comments
        )

    def _update_approval_status(
        self,
        request_id: str,
        status: str,
        reviewer_id: str,
        comments: str
    ) -> bool:
        """
        Update approval request status

        Args:
            request_id: Approval request ID
            status: New status
            reviewer_id: ID of the reviewer
            comments: Reviewer comments

        Returns:
            True if update was successful
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE approval_requests
                SET status = ?, reviewed_at = CURRENT_TIMESTAMP,
                    reviewer_id = ?, reviewer_comments = ?
                WHERE id = ?
            """, (status, reviewer_id, comments, request_id))

            connection.commit()
            close_db_connection(connection)

            self.logger.info(f"Approval request {request_id} updated to status: {status}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating approval request: {e}")
            return False

    def get_pending_requests(self, priority: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get pending approval requests

        Args:
            priority: Filter by priority (optional)

        Returns:
            List of pending approval requests
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if priority:
                cursor.execute("""
                    SELECT * FROM approval_requests
                    WHERE status = 'pending' AND priority = ?
                    ORDER BY created_at ASC
                """, (priority,))
            else:
                cursor.execute("""
                    SELECT * FROM approval_requests
                    WHERE status = 'pending'
                    ORDER BY created_at ASC
                """)

            results = cursor.fetchall()
            close_db_connection(connection)

            return [dict(row) for row in results]

        except Exception as e:
            self.logger.error(f"Error retrieving pending requests: {e}")
            return []

    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of an approval request

        Args:
            request_id: Approval request ID

        Returns:
            Request details or None if not found
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT * FROM approval_requests WHERE id = ?
            """, (request_id,))

            result = cursor.fetchone()
            close_db_connection(connection)

            return dict(result) if result else None

        except Exception as e:
            self.logger.error(f"Error retrieving request status: {e}")
            return None
