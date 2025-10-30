"""
Configuration for API keys and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# W&B / Weave Configuration
# Note: W&B Inference (for open-source models) uses the same WANDB_API_KEY as Weave tracing
WANDB_API_KEY = os.getenv("WANDB_API_KEY", "")
WEAVE_API_KEY = WANDB_API_KEY  # Alias for backward compatibility
WEAVE_BASE_URL = os.getenv("WEAVE_BASE_URL", "")

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Storage Configuration
STORAGE_MODE = os.getenv("STORAGE_MODE", "json")  # json, csv, supabase, or both

# Weave Tracing Configuration  
WEAVE_PROJECT_NAME = os.getenv("WEAVE_PROJECT_NAME", "g-tsvetkova-minerva-university/Testing-ar")
ENABLE_WEAVE_TRACING = os.getenv("ENABLE_WEAVE_TRACING", "true").lower() == "true"

# Model configurations
MODELS_CONFIG = {
    "gemini": {
        "name": "gemini-flash-latest",  # Flash latest - fast and works with Arabic
        "provider": "google",
        "api_key_env": "GOOGLE_API_KEY"
    },
    "claude": {
        "name": "claude-3-5-haiku-20241022",
        "provider": "anthropic",
        "api_key_env": "ANTHROPIC_API_KEY"
    },
    "qwen": {
        "name": "openai/gpt-oss-20b",  # W&B Inference - OpenAI open-source 20B model
        "provider": "wandb",  # Uses W&B Inference API
        "api_key_env": "WANDB_API_KEY"  # Same key as Weave tracing
    }
}

# Test configuration
MAX_CONVERSATION_TURNS = 10
CUSTOMER_SIMULATOR_MODEL = "gemini"  # Use Gemini for customer simulation by default
TEMPERATURE_CUSTOMER = 0.8  # Higher for natural variation
TEMPERATURE_AGENT = 0.7  # Standard for agent

# Evaluation configuration
ENABLE_LLM_JUDGE = True
JUDGE_MODEL = "claude"  # Use Claude for evaluation

# Output configuration
RESULTS_DIR = "results"
LOGS_DIR = "logs"

