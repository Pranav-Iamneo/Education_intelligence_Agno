"""
Assessment Agent - Agno Framework
Evaluates student knowledge and identifies skill levels
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class AssessmentAgent(Agent):
    """Assessment Agent using Agno"""

    def __init__(self):
        """Initialize Assessment Agent"""
        super().__init__(
            name="AssessmentAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert educational assessment specialist.
            Your role is to:
            1. Analyze student quiz/test responses
            2. Identify correct vs incorrect answers
            3. Recognize knowledge gaps and misconceptions
            4. Measure proficiency in specific topics
            5. Calculate accuracy percentages
            6. Determine overall skill level (Beginner/Intermediate/Advanced)

            Guidelines:
            - Be thorough in evaluating understanding
            - Identify both conceptual and procedural knowledge gaps
            - Provide constructive feedback highlighting both strengths and areas for improvement
            - Consider difficulty level when assessing
            - Give confidence scores for each topic
            - Be encouraging while being honest about areas needing work""",
            markdown=True
        )

    def assess_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess student knowledge and skills

        Args:
            student_data: Student assessment information

        Returns:
            Assessment analysis
        """
        prompt = f"""Analyze this student assessment:

Student: {student_data.get('student_name', 'N/A')}
Subject: {student_data.get('subject', 'N/A')}
Difficulty Level: {student_data.get('difficulty_level', 'intermediate')}
Total Questions: {student_data.get('questions_count', 10)}

Assessment Data:
- Correct Answers: {student_data.get('correct_answers', 0)}
- Incorrect Answers: {student_data.get('incorrect_answers', 0)}
- Partial Answers: {student_data.get('partial_answers', 0)}

Please provide:
1. Overall accuracy percentage
2. Skill level determination (Beginner/Intermediate/Advanced)
3. Performance breakdown by topic (if applicable)
4. Identified strengths
5. Identified weaknesses and knowledge gaps
6. Confidence scores for each area
7. Misconceptions detected
8. Specific, actionable feedback for each weak area
9. Estimated effort needed to improve
10. Overall assessment summary

Format with clear sections and bullet points."""

        try:
            response = self.run(prompt)
            logger.info(f"Assessment completed for: {student_data.get('student_name')}")

            # Extract content from response
            response_content = response.content if hasattr(response, 'content') else str(response)

            return {
                "status": "success",
                "analysis": response_content
            }
        except Exception as e:
            logger.error(f"Assessment error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
assessment_agent = AssessmentAgent()
