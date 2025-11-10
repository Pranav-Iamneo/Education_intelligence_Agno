"""
Progress Tracking Agent - Agno Framework
Monitors and analyzes student learning progress over time
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class ProgressAgent(Agent):
    """Progress Tracking Agent using Agno"""

    def __init__(self):
        """Initialize Progress Agent"""
        super().__init__(
            name="ProgressAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert learning analytics specialist and educational psychologist.
            Your role is to:
            1. Track learning metrics and progress over time
            2. Analyze improvement trends and patterns
            3. Measure goal achievement and milestone completion
            4. Identify struggling areas and learning plateaus
            5. Recognize and celebrate progress and achievements
            6. Suggest targeted interventions and adjustments

            Guidelines:
            - Use data-driven insights to identify trends
            - Celebrate progress while identifying areas for improvement
            - Be encouraging and motivational in tone
            - Detect early warning signs of struggle
            - Suggest specific interventions based on data patterns
            - Account for external factors affecting progress
            - Provide realistic projections for goal achievement
            - Track both quantitative and qualitative improvements""",
            markdown=True
        )

    def analyze_progress(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze student progress

        Args:
            student_data: Student progress data

        Returns:
            Progress analysis
        """
        prompt = f"""Analyze the learning progress for this student:

Student: {student_data.get('student_name', 'N/A')}
Subject: {student_data.get('subject', 'N/A')}

Assessment History:
- Initial Score: {student_data.get('initial_score', 'N/A')}
- Current Score: {student_data.get('current_score', 'N/A')}
- Number of Assessments: {student_data.get('assessments_completed', 0)}
- Time Period: {student_data.get('study_weeks', 'N/A')} weeks

Learning Activity:
- Topics Completed: {student_data.get('topics_completed', 0)}
- Total Topics: {student_data.get('total_topics', 0)}
- Practice Hours: {student_data.get('practice_hours', 0)}
- Average Daily Study: {student_data.get('daily_study_minutes', 0)} minutes

Milestone Status:
- Completed: {student_data.get('milestones_completed', 0)}
- In Progress: {student_data.get('milestones_in_progress', 0)}
- Remaining: {student_data.get('milestones_remaining', 0)}

Please provide:
1. Overall progress score and summary
2. Improvement rate and trajectory analysis
3. Topic-by-topic progress breakdown
4. Strengths and improvements achieved
5. Areas still needing work
6. Progress trends (accelerating/steady/plateauing/declining)
7. Detected learning patterns
8. Milestone achievement analysis
9. Estimated time to goal completion
10. Specific recommendations for optimization
11. Motivational assessment and encouragement
12. Risk factors or areas of concern

Format with clear sections, data-backed insights, and actionable recommendations."""

        try:
            response = self.run(prompt)
            logger.info(f"Progress analysis completed for: {student_data.get('student_name')}")

            # Extract content from response
            response_content = response.content if hasattr(response, 'content') else str(response)

            return {
                "status": "success",
                "analysis": response_content
            }
        except Exception as e:
            logger.error(f"Progress analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
progress_agent = ProgressAgent()
