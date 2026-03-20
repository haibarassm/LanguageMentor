from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel

from .base_agent import BaseAgent


class ConversationAgent(BaseAgent):
    """
    对话代理类，负责处理与用户的对话。
    """
    @property
    def name(self) -> str:
        """Get the agent name."""
        return "conversation"

    @property
    def prompt_file(self) -> str:
        """Get the prompt file path."""
        return "prompts/conversation_prompt.txt"

    def __init__(self, llm: BaseChatModel, session_id: Optional[str] = None):
        """
        Initialize the conversation agent.

        Args:
            llm: Language model instance to use for chat
            session_id: Optional session ID for conversation history
        """
        super().__init__(llm, session_id)

    def _get_initial_message(self) -> str:
        """
        Get the initial message for a new session.

        Returns:
            Initial message string
        """
        return "欢迎！今天有什么我能帮忙的吗？"
