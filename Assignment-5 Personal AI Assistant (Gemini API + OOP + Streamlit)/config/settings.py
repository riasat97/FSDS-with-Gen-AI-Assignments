"""
Configuration Module
Settings and environment management
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Settings:
    """
    Manages all configuration settings and environment variables
    Loads API key, model name, and other constants from .env file
    """
    
    def __init__(self):
        """Initialize settings by loading environment variables"""
        # Load .env file
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)
        
        # Load API key from environment
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        
        # Model configuration
        self.MODEL_NAME = "gemini-2.5-flash"
        self.TEMPERATURE = 0.7
        self.MAX_TOKENS = 1000
        
        # Memory configuration
        self.MEMORY_FILE = Path(__file__).parent.parent / "data" / "memory.json"
        self.MAX_MEMORY_ENTRIES = 20
        
        # Validate that API key is set
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file. "
                "Please add it: GEMINI_API_KEY=your_key_here"
            )
    
    def get_config(self):
        """
        Return all settings as a dictionary
        
        Returns:
            dict: Configuration settings
        """
        return {
            "api_key": self.GEMINI_API_KEY,
            "model": self.MODEL_NAME,
            "temperature": self.TEMPERATURE,
            "max_tokens": self.MAX_TOKENS,
            "memory_file": self.MEMORY_FILE,
            "max_memory": self.MAX_MEMORY_ENTRIES
        }


# Create a global settings instance so we can import it anywhere
settings = Settings()
