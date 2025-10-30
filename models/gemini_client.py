"""
Google Gemini client wrapper
"""

import time
from typing import List, Dict, Optional
import google.generativeai as genai
from .base_model import BaseModel

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


class GeminiClient(BaseModel):
    """Client for Google Gemini models"""
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-flash-latest"
    ):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google API key
            model_name: Gemini model name
        """
        super().__init__(model_name, api_key)
        genai.configure(api_key=api_key)
        
        # Configure safety settings to be less restrictive
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        # System instruction to frame Arabic content context (reduces false positives)
        system_instruction = """You are participating in a customer service quality evaluation research project. 
You will be analyzing and generating authentic customer service conversations in Egyptian Arabic dialect.
These are legitimate business communications for training and evaluation purposes.
The conversations discuss common e-commerce topics like delivery, orders, and customer service interactions.
All content is benign professional communication and should be processed normally."""
        
        self.model = genai.GenerativeModel(
            model_name,
            safety_settings=safety_settings,
            system_instruction=system_instruction
        )
        
    @property
    def provider_name(self) -> str:
        return "google_gemini"
    
    @weave.op() if WEAVE_AVAILABLE else lambda f: f
    def generate_response(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> Dict[str, any]:
        """Generate response from Gemini"""
        
        try:
            start_time = time.time()
            
            # Construct the full conversation
            messages = []
            
            # Add system prompt as first user message
            messages.append({
                "role": "user",
                "parts": [system_prompt]
            })
            messages.append({
                "role": "model",
                "parts": ["فهمت، أنا جاهزة للمساعدة."]  # Arabic: "Understood, I'm ready to help."
            })
            
            # Add conversation history
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                messages.append({
                    "role": role,
                    "parts": [msg["content"]]
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "parts": [user_message]
            })
            
            # Generate response with safety settings
            chat = self.model.start_chat(history=messages[:-1])
            
            # Safety settings for this request
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            response = chat.send_message(
                user_message,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
                safety_settings=safety_settings
            )
            
            latency = time.time() - start_time
            
            # Check if response was blocked
            if not response.candidates:
                error_msg = f"Response blocked by safety filters: {response.prompt_feedback}"
                raise Exception(error_msg)
            
            if not response.text:
                finish_reason = response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
                error_msg = f"Empty response. Finish reason: {finish_reason}"
                raise Exception(error_msg)
            
            # Extract tokens used (approximate)
            tokens_used = response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
            
            self._record_request(tokens_used, latency)
            
            return {
                "response": response.text,
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

