"""
Weave client wrapper for Qwen open-source model
"""

import time
import os
from typing import List, Dict, Optional
import requests
from openai import OpenAI
from .base_model import BaseModel

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


class WeaveClient(BaseModel):
    """Client for W&B Inference with open-source models"""
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "openai/gpt-oss-20b",
        base_url: str = None
    ):
        """
        Initialize Weave client for W&B Inference
        
        Args:
            api_key: WANDB_API_KEY for Weave inference service
            model_name: Qwen model name
            base_url: Base URL for W&B Inference API (defaults to W&B)
        """
        super().__init__(model_name, api_key)
        
        # Use W&B Inference API endpoint if no base_url provided
        if not base_url:
            base_url = "https://api.inference.wandb.ai/v1"
        
        self.base_url = base_url
        
        # Get W&B project name for inference
        project_name = os.getenv("WEAVE_PROJECT_NAME", "Testing-ar")
        
        # Initialize OpenAI client with W&B Inference settings
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            default_headers={"X-WANDB-PROJECT": project_name}
        )
        
    @property
    def provider_name(self) -> str:
        return "weave_qwen"
    
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def generate_response(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Dict[str, any]:
        """Generate response from Qwen via Weave/Together"""
        
        try:
            start_time = time.time()
            
            # Construct messages
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
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
            
            # Generate response using OpenAI-compatible API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            latency = time.time() - start_time
            
            # Extract tokens used
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
            
            # Check for empty/None response
            content = response.choices[0].message.content
            if content is None or content.strip() == "":
                raise Exception("Model returned empty/None response. This can happen with certain models - try again or use a different model.")
            
            self._record_request(tokens_used, latency)
            
            return {
                "response": content,
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

