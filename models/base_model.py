"""
Base Model class for all AI model clients
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time


class BaseModel(ABC):
    """Base class for all AI model clients"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        Initialize model client
        
        Args:
            model_name: Name/identifier of the model
            api_key: API key for the model provider
        """
        self.model_name = model_name
        self.api_key = api_key
        self.total_tokens = 0
        self.total_requests = 0
        self.total_latency = 0.0
        
    @abstractmethod
    def generate_response(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Dict[str, any]:
        """
        Generate response from the model
        
        Args:
            system_prompt: System prompt for the agent
            conversation_history: Previous conversation history
            user_message: Current user message
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary containing:
                - response: Generated text response
                - tokens_used: Number of tokens used
                - latency: Time taken in seconds
                - error: Error message if any
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Provider name (e.g., 'google', 'anthropic', 'weave')"""
        pass
    
    def get_stats(self) -> Dict[str, any]:
        """
        Get usage statistics
        
        Returns:
            Dictionary with usage stats
        """
        return {
            "model_name": self.model_name,
            "provider": self.provider_name,
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "total_latency": self.total_latency,
            "avg_latency": self.total_latency / self.total_requests if self.total_requests > 0 else 0
        }
    
    def reset_stats(self):
        """Reset usage statistics"""
        self.total_tokens = 0
        self.total_requests = 0
        self.total_latency = 0.0
    
    def _record_request(self, tokens: int, latency: float):
        """
        Record request statistics
        
        Args:
            tokens: Tokens used in request
            latency: Latency in seconds
        """
        self.total_requests += 1
        self.total_tokens += tokens
        self.total_latency += latency

