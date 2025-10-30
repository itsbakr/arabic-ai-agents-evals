"""
Weave initialization and tracing utilities
"""

import os
from typing import Optional, Callable
import config

# Global flag to track if Weave is initialized
_weave_initialized = False
_weave_available = False

try:
    import weave
    _weave_available = True
except ImportError:
    print("⚠️ Weave not installed. Run: pip install weave")
    _weave_available = False


def initialize_weave(project_name: Optional[str] = None) -> bool:
    """
    Initialize Weave tracing for the project
    
    Args:
        project_name: Name of the Weave project (default from config)
        
    Returns:
        True if successfully initialized
    """
    global _weave_initialized
    
    if not config.ENABLE_WEAVE_TRACING:
        print("ℹ️ Weave tracing disabled in config")
        return False
    
    if not _weave_available:
        print("⚠️ Weave package not available")
        return False
    
    if _weave_initialized:
        print("ℹ️ Weave already initialized")
        return True
    
    try:
        # Get project name
        project_name = project_name or config.WEAVE_PROJECT_NAME
        
        # Ensure WANDB_API_KEY is set in environment
        wandb_key = os.getenv('WANDB_API_KEY')
        if not wandb_key:
            print(f"⚠️ WANDB_API_KEY not found in environment")
            print(f"   Set it with: export WANDB_API_KEY=your_key")
            print(f"   Or add to .env file")
            return False
        
        # Set the API key explicitly
        os.environ['WANDB_API_KEY'] = wandb_key
        
        # Project name already includes entity if needed (e.g., "entity/project")
        # No need to add entity if already included
        full_project = project_name
        
        # Initialize Weave (correct syntax from docs)
        weave.init(full_project)
        _weave_initialized = True
        
        print(f"✅ Weave tracing initialized: {full_project}")
        print(f"📊 View traces at: https://wandb.ai/{full_project}/weave")
        return True
        
    except Exception as e:
        print(f"⚠️ Weave initialization failed: {str(e)}")
        print(f"   Continuing without tracing...")
        return False


def weave_trace(name: Optional[str] = None):
    """
    Decorator to trace functions with Weave
    
    Args:
        name: Optional name for the trace
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        if not _weave_available or not config.ENABLE_WEAVE_TRACING:
            # Return original function if Weave not available
            return func
        
        try:
            # Use Weave's op decorator
            return weave.op(name=name or func.__name__)(func)
        except:
            # If decoration fails, return original function
            return func
    
    return decorator


def log_to_weave(data: dict, name: str = "log"):
    """
    Log arbitrary data to Weave
    
    Args:
        data: Dictionary of data to log
        name: Name for the log entry
    """
    if not _weave_available or not config.ENABLE_WEAVE_TRACING or not _weave_initialized:
        return
    
    try:
        weave.log({name: data})
    except:
        pass  # Silently fail if logging fails


def get_weave_status() -> dict:
    """Get current Weave status"""
    return {
        "available": _weave_available,
        "initialized": _weave_initialized,
        "enabled": config.ENABLE_WEAVE_TRACING,
        "project": config.WEAVE_PROJECT_NAME if _weave_initialized else None
    }

