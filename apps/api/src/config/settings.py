"""
Application configuration loaded from environment variables using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Find the .env file - check both apps/api/ and project root
_api_root = Path(__file__).parent.parent.parent
_project_root = _api_root.parent.parent
_env_file = _api_root / ".env"
if not _env_file.exists():
    _env_file = _project_root / ".env"

class Settings(BaseSettings):
    """Central configuration for all external services."""
    model_config = SettingsConfigDict(env_file=str(_env_file), env_file_encoding='utf-8', extra='ignore')

    # Google GenAI (Free Tier)
    google_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_service_role_key: str = ""

    # Neo4j
    neo4j_uri: str = ""
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # Bhashini
    bhashini_api_key: str = ""
    bhashini_user_id: str = ""

    # App
    python_env: str = "development"
    
    @property
    def debug(self) -> bool:
        return self.python_env == "development"

settings = Settings()
