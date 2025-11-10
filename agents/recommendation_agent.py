"""
Recommendation Engine Agent - Agno Framework
Provides AI-driven learning recommendations and personalized suggestions
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class RecommendationAgent(Agent):
    """Recommendation Engine Agent using Agno"""

    def __init__(self):
        """Initialize Recommendation Engine Agent"""
        super().__init__(
            name="RecommendationAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert educational advisor and career guidance counselor.
            Your role is to:
            1. Recommend next topics to study based on progress
            2. Suggest proven and effective study techniques
            3. Recommend similar or alternative content
            4. Find and suggest peer study groups
            5. Recommend tools, apps, and resources
            6. Provide career path guidance aligned with learning goals

            Guidelines:
            - Make recommendations based on learning style and preferences
            - Suggest tools and techniques with documented effectiveness
            - Consider student's career aspirations
            - Identify synergies between topics and career paths
            - Predict success factors based on data
            - Provide multiple options/alternatives
            - Explain the 'why' behind recommendations
            - Be encouraging and supportive
            - Consider time and resource constraints""",
            markdown=True
        )

    def get_recommendations(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized learning recommendations

        Args:
            student_data: Student profile, history, and goals

        Returns:
            Recommendations
        """
        prompt = f"""Provide personalized learning recommendations for this student:

Student: {student_data.get('student_name', 'N/A')}
Subject: {student_data.get('subject', 'N/A')}
Current Level: {student_data.get('skill_level', 'Intermediate')}
Learning Style: {student_data.get('learning_style', 'mixed')}
Weak Areas: {student_data.get('weak_areas', 'N/A')}
Strong Areas: {student_data.get('strong_areas', 'N/A')}
Career Interests: {student_data.get('career_interests', 'Not specified')}
Available Time: {student_data.get('hours_per_week', 5)} hours/week
Previous Attempts: {student_data.get('previous_assessments', 0)}

Please provide:
1. Next topic recommendation (with justification)
2. Why this topic is important
3. Prerequisites check (are prerequisites met?)
4. Recommended study techniques:
   - Most effective for this student
   - Alternative techniques
   - Research-backed methods
5. Resource recommendations:
   - Video platforms and specific courses
   - Books and textbooks
   - Interactive tools and software
   - Podcasts and audio resources
6. Similar/alternative content:
   - Different learning formats
   - Alternative approaches
   - Supplementary materials
7. Study group recommendations:
   - Group matching criteria
   - Where to find groups
   - Benefits of peer learning
8. Tool recommendations:
   - Practice and quiz platforms
   - Visualization tools
   - Productivity tools
   - Community forums
9. Career path alignment:
   - How this topic helps career goals
   - Related career paths
   - Industry relevance
   - Skill building progression
10. Success factors:
    - Key elements for success in this topic
    - Potential challenges and how to overcome them
    - Estimated difficulty level
    - Success probability based on profile
11. Timeline and milestones
12. Motivational message

Format with clear sections, specific recommendations, and actionable next steps."""

        try:
            response = self.run(prompt)
            logger.info(f"Recommendations generated for: {student_data.get('student_name')}")

            # Extract content from response
            response_content = response.content if hasattr(response, 'content') else str(response)

            return {
                "status": "success",
                "analysis": response_content
            }
        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
recommendation_agent = RecommendationAgent()
