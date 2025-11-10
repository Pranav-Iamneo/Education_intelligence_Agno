"""
Learning Path Agent - Agno Framework
Recommends personalized learning paths based on student profile
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class LearningPathAgent(Agent):
    """Learning Path Agent using Agno"""

    def __init__(self):
        """Initialize Learning Path Agent"""
        super().__init__(
            name="LearningPathAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert educational curriculum designer and learning specialist.
            Your role is to:
            1. Design custom, personalized learning routes for each student
            2. Recommend high-quality resources (videos, books, interactive tools)
            3. Sequence topics logically from foundational to advanced
            4. Estimate realistic time needed for each section
            5. Set achievable learning milestones
            6. Adapt learning paths based on student progress

            Guidelines:
            - Personalize based on student's learning style and preferences
            - Consider available time and commitment level
            - Recommend proven, effective learning resources
            - Create achievable milestones to maintain motivation
            - Balance challenge with confidence-building
            - Include variety in learning methods (videos, practice, theory, projects)
            - Build from weakness areas identified in assessment
            - Provide clear daily/weekly study recommendations""",
            markdown=True
        )

    def recommend_learning_path(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend personalized learning path

        Args:
            student_data: Student profile and assessment results

        Returns:
            Learning path recommendation
        """
        prompt = f"""Create a personalized learning path for this student:

Student: {student_data.get('student_name', 'N/A')}
Subject: {student_data.get('subject', 'N/A')}
Current Level: {student_data.get('skill_level', 'Intermediate')}
Goal Level: {student_data.get('target_level', 'Advanced')}
Learning Style: {student_data.get('learning_style', 'mixed')}
Available Time: {student_data.get('hours_per_week', 5)} hours per week
Weak Areas: {student_data.get('weak_areas', 'N/A')}
Strong Areas: {student_data.get('strong_areas', 'N/A')}

Please provide:
1. Recommended topic sequence (from foundational to advanced)
2. Estimated completion timeline
3. Daily/weekly study schedule and time breakdown
4. Resource recommendations:
   - Video tutorials (with specific titles/platforms)
   - Textbooks and study materials
   - Interactive practice tools
   - Real-world projects
5. Weekly milestones and checkpoints
6. Specific practice problems or exercises recommended
7. Difficulty progression strategy
8. Integration opportunities (how topics connect)
9. Review and reinforcement schedule
10. Success checklist and assessment points

Format with clear sections, timelines, and specific resources."""

        try:
            response = self.run(prompt)
            logger.info(f"Learning path generated for: {student_data.get('student_name')}")

            # Extract content from response
            response_content = response.content if hasattr(response, 'content') else str(response)

            return {
                "status": "success",
                "analysis": response_content
            }
        except Exception as e:
            logger.error(f"Learning path generation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
learning_path_agent = LearningPathAgent()
