"""
Memory Module
Handles conversation memory and persistence
"""

import json
from pathlib import Path
from typing import List, Dict
from config.settings import settings
from jarvis.logger import get_logger

logger = get_logger(__name__)


class Memory:
    """
    Manages conversation history storage and retrieval
    Saves conversations to JSON file for persistence
    Loads conversation history when app starts
    
    Attributes:
        memory_file: Path to JSON file storing conversations
        conversations: List of conversation messages in memory
    """
    
    def __init__(self):
        """Initialize Memory and load existing conversations from file"""
        self.memory_file = settings.MEMORY_FILE
        self.conversations = []
        
        # Create data directory if it doesn't exist
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing conversations
        self._load_from_file()
        
        logger.info("Memory initialized (%s messages loaded)", len(self.conversations))
    
    def add(self, role: str, content: str) -> None:
        """
        Add a message to conversation history
        
        Args:
            role (str): "user" or "assistant"
            content (str): The message content
        """
        message = {
            "role": role.lower(),
            "content": content
        }
        self.conversations.append(message)
        
        # Save to file after each message
        self._save_to_file()
    
    def get_history(self, limit: int = None) -> List[Dict]:
        """
        Get conversation history
        
        Args:
            limit (int, optional): Max number of messages to return (most recent)
            
        Returns:
            List[Dict]: List of conversation messages
        """
        if limit is None:
            limit = settings.MAX_MEMORY_ENTRIES
        
        # Return most recent conversations up to limit
        return self.conversations[-limit:] if self.conversations else []
    
    def clear(self) -> str:
        """
        Clear all conversation history
        
        Returns:
            str: Confirmation message
        """
        self.conversations = []
        self._save_to_file()
        return "✓ Memory cleared"
    
    def get_summary(self) -> Dict:
        """
        Get memory statistics
        
        Returns:
            Dict: Statistics about stored conversations
        """
        return {
            "total_messages": len(self.conversations),
            "user_messages": len([m for m in self.conversations if m["role"] == "user"]),
            "assistant_messages": len([m for m in self.conversations if m["role"] == "assistant"]),
            "memory_file": str(self.memory_file)
        }
    
    def _save_to_file(self) -> None:
        """Save conversations to JSON file"""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.conversations, f, indent=2)
        except Exception as e:
            logger.exception("Error saving memory: %s", e)
    
    def _load_from_file(self) -> None:
        """Load conversations from JSON file if it exists"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, "r") as f:
                    self.conversations = json.load(f)
            else:
                self.conversations = []
        except Exception as e:
            logger.exception("Error loading memory: %s", e)
            self.conversations = []
