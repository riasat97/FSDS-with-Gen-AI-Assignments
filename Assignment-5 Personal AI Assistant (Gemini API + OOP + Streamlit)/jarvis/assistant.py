"""
JARVIS Assistant Module
Main intelligence engine combining all components
"""

from jarvis.gemini_engine import GeminiEngine
from jarvis.prompt_controller import PromptController, AssistantRole
from jarvis.memory import Memory
from jarvis.errors import JarvisError
from jarvis.logger import get_logger

logger = get_logger(__name__)


class JarvisAssistant:
    """
    Main JARVIS Assistant class
    Orchestrates all components: GeminiEngine, PromptController, and Memory
    Coordinates the workflow from user input to AI response
    
    Attributes:
        engine: GeminiEngine instance for API communication
        controller: PromptController instance for prompt formatting
        memory: Memory instance for conversation persistence
    """
    
    def __init__(self):
        """
        Initialize JarvisAssistant by creating all component instances
        
        Raises:
            RuntimeError: If any component fails to initialize
        """
        try:
            # Initialize all components
            self.engine = GeminiEngine()
            self.controller = PromptController()
            self.memory = Memory()
            
            logger.info("JARVIS Assistant initialized successfully")
        
        except Exception as e:
            logger.exception("Failed to initialize JARVIS Assistant")
            raise
    
    def respond(self, user_input: str, *, prompt_hint: str | None = None, store_user_input: str | None = None) -> str:
        """
        Process user input and generate a response
        
        Workflow:
        1. Get conversation history from Memory
        2. Build complete prompt with PromptController
        3. Generate response with GeminiEngine
        4. Save user input and response to Memory
        5. Return response to user
        
        Args:
            user_input (str): The user's question or input
            prompt_hint (str, optional): Extra instruction appended to the prompt (not stored in memory)
            store_user_input (str, optional): What to store in memory for the user message (defaults to user_input)
            
        Returns:
            str: The assistant's response
        """
        try:
            # Step 1: Get conversation history
            history = self.memory.get_history()
            
            # Step 2: Build complete prompt with system instructions + history
            prompt_user_input = user_input
            if prompt_hint:
                prompt_user_input = f"{user_input}\n\n{prompt_hint}"
            full_prompt = self.controller.build_prompt(prompt_user_input, history)
            
            # Step 3: Generate response from Gemini
            response = self.engine.generate(full_prompt)
            
            # Step 4: Save to memory
            self.memory.add("user", store_user_input if store_user_input is not None else user_input)
            self.memory.add("assistant", response)
            
            # Step 5: Return response
            return response
        
        except JarvisError:
            # Already classified; log and re-raise for UI to display.
            logger.exception("JarvisError while generating response")
            raise
        except Exception as e:
            logger.exception("Unexpected error while generating response")
            raise JarvisError("❌ Something went wrong while generating a response. Please try again.", technical_message=str(e))
    
    def respond_stream(self, user_input: str):
        """
        Process user input and generate response with streaming
        Yields response chunks as they arrive from the API
        
        Args:
            user_input (str): The user's question or input
            
        Yields:
            str: Response chunks
        """
        try:
            # Get conversation history
            history = self.memory.get_history()
            
            # Build complete prompt
            full_prompt = self.controller.build_prompt(user_input, history)
            
            # Stream response from Gemini
            full_response = ""
            for chunk in self.engine.generate_stream(full_prompt):
                full_response += chunk
                yield chunk
            
            # Save to memory after streaming is complete
            self.memory.add("user", user_input)
            self.memory.add("assistant", full_response)
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            yield error_msg
    
    def set_role(self, role: AssistantRole) -> str:
        """
        Change the assistant's role/personality
        
        Args:
            role (AssistantRole): The new role to set
            
        Returns:
            str: Confirmation message
        """
        return self.controller.set_role(role)
    
    def get_available_roles(self):
        """
        Get list of available roles
        
        Returns:
            dict: Mapping of role names to display names
        """
        roles = {}
        for role in AssistantRole:
            roles[role.value] = role.value.capitalize()
        return roles
    
    def get_memory_summary(self):
        """
        Get statistics about conversation memory
        
        Returns:
            dict: Memory statistics
        """
        summary = self.memory.get_summary()
        return {
            "total_messages": summary["total_messages"],
            "user_messages": summary["user_messages"],
            "assistant_messages": summary["assistant_messages"]
        }
    
    def clear_memory(self) -> str:
        """
        Clear all conversation history
        
        Returns:
            str: Confirmation message
        """
        return self.memory.clear()
    
    def get_conversation_history(self):
        """
        Get full conversation history
        
        Returns:
            list: List of conversation messages
        """
        return self.memory.get_history()
    
    def export_conversation(self, format: str = "json") -> str:
        """
        Export conversation to string format
        
        Args:
            format (str): "json" or "txt"
            
        Returns:
            str: Formatted conversation data
        """
        import json
        from datetime import datetime
        
        history = self.memory.get_history()
        
        if format == "json":
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "total_messages": len(history),
                "conversations": history
            }
            return json.dumps(export_data, indent=2)
        
        elif format == "txt":
            lines = []
            lines.append("=" * 60)
            lines.append("JARVIS Conversation Export")
            lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"Total Messages: {len(history)}")
            lines.append("=" * 60)
            lines.append("")
            
            for msg in history:
                role = "You" if msg["role"] == "user" else "JARVIS"
                lines.append(f"{role}:")
                lines.append(msg["content"])
                lines.append("")
            
            return "\n".join(lines)
        
        else:
            raise ValueError("Format must be 'json' or 'txt'")
