"""
Application configuration loaded from environment variables.
"""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Central configuration for all external services."""

    # Google Gemini
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")

    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Neo4j
    neo4j_uri: str = os.getenv("NEO4J_URI", "")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "")

    # Bhashini
    bhashini_api_key: str = os.getenv("BHASHINI_API_KEY", "")
    bhashini_user_id: str = os.getenv("BHASHINI_USER_ID", "")

    # App
    environment: str = os.getenv("PYTHON_ENV", "development")
    debug: bool = os.getenv("PYTHON_ENV", "development") == "development"


settings = Settings()
