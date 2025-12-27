"""
Gemini API Engine Module
Handles communication with Google Gemini API
"""

import google.generativeai as genai
from config.settings import settings
from jarvis.errors import GeminiQuotaExceededError, GeminiRequestError
from jarvis.logger import get_logger

logger = get_logger(__name__)


class GeminiEngine:
    """
    Encapsulates Google Gemini API interactions
    Handles model initialization, response generation, and error handling
    
    Attributes:
        model: The generative model instance
        api_key: API key from settings
        model_name: Model name from settings
    """
    
    def __init__(self):
        """
        Initialize Gemini Engine with API key and model from settings
        
        Raises:
            RuntimeError: If API configuration fails
        """
        try:
            # Get settings
            self.api_key = settings.GEMINI_API_KEY
            self.model_name = settings.MODEL_NAME
            
            # Configure the Gemini API
            genai.configure(api_key=self.api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel(self.model_name)
            
            logger.info("Gemini Engine initialized with model: %s", self.model_name)
        
        except Exception as e:
            logger.exception("Failed to initialize Gemini Engine")
            raise GeminiRequestError(
                "Failed to initialize the Gemini client. Check your API key and internet connection.",
                technical_message=str(e),
            )

    def _classify_and_raise(self, exc: Exception) -> None:
        msg = str(exc) or exc.__class__.__name__
        msg_lower = msg.lower()

        # Common quota / rate / resource exhaustion signals across Gemini SDKs.
        quota_markers = [
            "resource_exhausted",
            "quota",
            "429",
            "rate limit",
            "too many requests",
            "exceeded",
        ]
        if any(m in msg_lower for m in quota_markers):
            raise GeminiQuotaExceededError(
                "⚠️ Gemini API limit reached (quota/rate limit). Please wait and try again, or use a different API key.",
                technical_message=msg,
            )

        raise GeminiRequestError(
            "❌ Gemini request failed. Please try again.",
            technical_message=msg,
        )
    
    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and get a response
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            str: The model's response
            
        Raises:
            RuntimeError: If API call fails
        """
        try:
            # Generate content with settings
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_TOKENS
                )
            )
            
            # Return the response text
            return response.text
        
        except Exception as e:
            logger.exception("Gemini generate() failed")
            self._classify_and_raise(e)
    
    def test_connection(self) -> bool:
        """
        Test if API connection is working
        
        Returns:
            bool: True if connection successful
        """
        try:
            response = self.generate("Hi")
            return bool(response)
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def generate_stream(self, prompt: str):
        """
        Generate response with streaming (word-by-word)
        
        Args:
            prompt (str): The prompt to send to the model
            
        Yields:
            str: Response chunks as they arrive
        """
        try:
            response = self.model.generate_content(
                prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_TOKENS
                )
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.exception("Gemini generate_stream() failed")
            # Streaming callers can choose to show the chunked error; keep it short but informative.
            try:
                self._classify_and_raise(e)
            except Exception as classified:
                yield f"Error: {getattr(classified, 'user_message', str(classified))}"
