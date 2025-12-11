"""
Configuration with all tracing options
"""

import os
from dotenv import load_dotenv
import logging

load_dotenv()

# ============= LOGGING CONFIGURATION =============
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('resume_screening.log'),  # Save to file
        logging.StreamHandler()  # Also print to console
    ]
)

# ============= ENVIRONMENT VARIABLES =============

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")

# Tracing Configuration
ENABLE_DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENABLE_LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING", "true").lower() == "true"
ENABLE_CREW_DEBUG = os.getenv("CREW_DEBUG", "true").lower() == "true"

# LangChain Tracing Setup
if ENABLE_LANGCHAIN_TRACING:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = "Resume-Screening-System"

# App Configuration
APP_NAME = os.getenv("APP_NAME", "Resume Screening System")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEFAULT_JOB_TITLE = os.getenv("DEFAULT_JOB_TITLE", "Software Engineer")
DEFAULT_REQUIRED_EXPERIENCE = int(os.getenv("DEFAULT_REQUIRED_EXPERIENCE", "3"))

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-2-70b-chat")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

logger = logging.getLogger(__name__)
logger.info(f"Config loaded: {APP_NAME} v{APP_VERSION}")
logger.info(f"Tracing enabled: {ENABLE_LANGCHAIN_TRACING}")