"""
Education Intelligence System Configuration
Agno Framework with Gemini AI
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings:
    """Application settings"""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    AGENT_MODEL = "gemini-2.0-flash"

    # API Configuration
    API_PORT = int(os.getenv("API_PORT", "8083"))
    API_HOST = os.getenv("API_HOST", "localhost")

    # Database Configuration
    DB_FILE = os.getenv("DATABASE", "education.db")

    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Application Metadata
    APP_NAME = "Education & Learning Intelligence System"
    APP_VERSION = "1.0.0"
    DESCRIPTION = "AI-powered student assessment, learning path recommendation, and progress tracking"

# Create settings instance
settings = Settings()
