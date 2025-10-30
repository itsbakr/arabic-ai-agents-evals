"""
Anthropic Claude client wrapper
"""

import time
from typing import List, Dict, Optional
from anthropic import Anthropic
from .base_model import BaseModel

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


class ClaudeClient(BaseModel):
    """Client for Anthropic Claude models"""
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "claude-3-5-haiku-20241022"
    ):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key
            model_name: Claude model name
        """
        super().__init__(model_name, api_key)
        self.client = Anthropic(api_key=api_key)
        
    @property
    def provider_name(self) -> str:
        return "anthropic_claude"
    
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def generate_response(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Dict[str, any]:
        """Generate response from Claude"""
        
        try:
            start_time = time.time()
            
            # Construct messages
            messages = []
            
            # Add conversation history
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Generate response
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=messages
            )
            
            latency = time.time() - start_time
            
            # Extract tokens used
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            self._record_request(tokens_used, latency)
            
            return {
                "response": response.content[0].text,
                "tokens_used": tokens_used,
                "latency": latency,
                "error": None
            }
            
        except Exception as e:
            latency = time.time() - start_time
            return {
                "response": None,
                "tokens_used": 0,
                "latency": latency,
                "error": str(e)
            }

