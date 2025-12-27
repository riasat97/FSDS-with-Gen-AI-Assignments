"""
Prompt Controller Module
Manages role-based assistant behaviors and prompts
"""

from enum import Enum
from typing import List, Dict


class AssistantRole(Enum):
    """Enum for different assistant roles"""
    GENERAL = "general"
    TUTOR = "tutor"
    CODER = "coder"
    CAREER = "career"


class PromptController:
    """
    Controls prompt formatting and system instructions
    Injects personality and context into prompts based on selected role
    
    Attributes:
        current_role: The current assistant role
        system_prompts: Dictionary of role-based system instructions
    """
    
    def __init__(self):
        """Initialize PromptController with role-based system prompts"""
        self.current_role = AssistantRole.GENERAL
        
        # Define system prompts for each role
        self.system_prompts = {
            AssistantRole.GENERAL: (
                "You are a helpful, friendly personal AI assistant. "
                "Provide clear, concise, and accurate responses. "
                "Be conversational and natural in your tone."
            ),
            AssistantRole.TUTOR: (
                "You are an expert educational tutor. "
                "Explain concepts clearly with examples. "
                "Ask questions to check understanding. "
                "Break down complex topics into simple steps."
            ),
            AssistantRole.CODER: (
                "You are an expert programmer and code reviewer. "
                "Provide code solutions with explanations. "
                "Follow best practices and clean code principles. "
                "Suggest optimizations when appropriate."
            ),
            AssistantRole.CAREER: (
                "You are a professional career coach and mentor. "
                "Provide advice on career growth, interviews, and development. "
                "Ask clarifying questions to understand the user's goals. "
                "Offer practical, actionable suggestions."
            )
        }
    
    def set_role(self, role: AssistantRole) -> str:
        """
        Set the current assistant role
        
        Args:
            role (AssistantRole): The role to set
            
        Returns:
            str: Confirmation message
        """
        self.current_role = role
        return f"✓ Role changed to: {role.value.capitalize()}"
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the current role
        
        Returns:
            str: System prompt for the current role
        """
        return self.system_prompts[self.current_role]
    
    def build_prompt(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """
        Build a complete prompt with system instructions and conversation context
        
        Args:
            user_input (str): The user's current question/input
            conversation_history (List[Dict], optional): Previous conversation messages
            
        Returns:
            str: Formatted prompt ready to send to Gemini
        """
        # Start with system prompt
        prompt = f"{self.get_system_prompt()}\n\n"
        
        # Add conversation history if provided
        if conversation_history:
            prompt += "Previous conversation:\n"
            for msg in conversation_history:
                role = msg.get("role", "").capitalize()
                content = msg.get("content", "")
                prompt += f"{role}: {content}\n"
            prompt += "\n"
        
        # Add current user input
        prompt += f"User: {user_input}"
        
        return prompt
    
    def get_available_roles(self) -> List[str]:
        """
        Get list of available roles
        
        Returns:
            List[str]: List of role names
        """
        return [role.value for role in AssistantRole]
