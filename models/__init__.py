"""
Model client wrappers for different AI providers
"""

from .base_model import BaseModel
from .gemini_client import GeminiClient

# Optional imports - only load if packages are installed
try:
    from .claude_client import ClaudeClient
except ImportError:
    ClaudeClient = None

try:
    from .weave_client import WeaveClient
except ImportError:
    WeaveClient = None

__all__ = [
    'BaseModel',
    'GeminiClient',
    'ClaudeClient',
    'WeaveClient',
]

