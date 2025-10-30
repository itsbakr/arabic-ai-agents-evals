"""
Base Agent class for all customer service agents
"""

from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all customer service agents"""
    
    def __init__(self, language: str = "arabic"):
        """
        Initialize base agent
        
        Args:
            language: Language for the agent (arabic or english)
        """
        self.language = language
        self.conversation_history: List[Dict[str, str]] = []
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the agent
        
        Returns:
            System prompt string
        """
        pass
    
    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """
        Get list of available actions/functions for the agent
        
        Returns:
            List of action names
        """
        pass
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Agent name"""
        pass
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Agent type identifier"""
        pass
    
    def add_to_history(self, role: str, content: str):
        """
        Add message to conversation history
        
        Args:
            role: Role (user or assistant)
            content: Message content
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get full conversation history
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history.copy()
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
    
    def simulate_action(self, action: str, *args, **kwargs) -> str:
        """
        Simulate an action/function call
        
        Args:
            action: Action name
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Simulated result as string
        """
        # This will be overridden by specific agents if needed
        return f"Action {action} executed successfully with args: {args}, kwargs: {kwargs}"

