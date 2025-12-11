"""
Configuration management for Resume Screening System
Loads and manages all application settings from environment
"""

from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Configuration
    openrouter_api_key: str  # OpenRouter API key
    openai_api_key: str = "sk-dummy-key-111"  # Dummy key (not used)
    
    # LLM Configuration
    llm_model: str = "openrouter/meta-llama/llama-3.1-8b-instruct"
    llm_base_url: str = "https://openrouter.ai/api/v1"
    
    # Application Settings
    app_name: str = "Resume Screening System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Job Configuration Defaults
    default_job_title: str = "Software Engineer"
    default_required_skills: List[str] = [
        "Python",
        "JavaScript",
        "React",
        "REST API",
        "SQL"
    ]
    default_required_experience: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Initialize global settings
settings = Settings()