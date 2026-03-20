"""Abstract base class for agents."""

from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from .session_history import get_session_history
from utils.logger import LOG


class BaseAgent(ABC):
    """
    Abstract base class for agents.

    This class provides common functionality for all agents, including:
    - Prompt loading from file
    - Chatbot creation with LLM injection
    - Session management
    """

    def __init__(self, llm: BaseChatModel, session_id: Optional[str] = None):
        """
        Initialize the agent.

        Args:
            llm: Language model instance to use for chat
            session_id: Optional session ID for conversation history
        """
        self.llm = llm
        self.session_id = session_id if session_id else self.name
        self.prompt = self.load_prompt()
        self.create_chatbot()

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the agent name.

        Returns:
            Agent name string
        """
        pass

    @property
    @abstractmethod
    def prompt_file(self) -> str:
        """
        Get the prompt file path.

        Returns:
            Path to the prompt file
        """
        pass

    def load_prompt(self) -> str:
        """
        Load system prompt from file.

        Returns:
            Prompt string

        Raises:
            FileNotFoundError: If prompt file is not found
        """
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")

    def create_chatbot(self) -> None:
        """Initialize the chatbot with system prompt and LLM."""
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])

        self.chatbot = system_prompt | self.llm
        self.chatbot_with_history = RunnableWithMessageHistory(
            self.chatbot, get_session_history
        )

    def start_new_session(self) -> str:
        """
        Start a new session and return initial AI message.

        Returns:
            Initial AI message
        """
        history = get_session_history(self.session_id)
        LOG.debug(f"[history]:{history}")

        if not history.messages:
            initial_ai_message = self._get_initial_message()
            history.add_message(AIMessage(content=initial_ai_message))
            return initial_ai_message
        else:
            return history.messages[-1].content

    @abstractmethod
    def _get_initial_message(self) -> str:
        """
        Get the initial message for a new session.

        Returns:
            Initial message string
        """
        pass

    def chat_with_history(self, user_input: str) -> str:
        """
        Process user input and generate response with chat history.

        Args:
            user_input: User input message

        Returns:
            AI generated response
        """
        from langchain_core.messages import HumanMessage

        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            {"configurable": {"session_id": self.session_id}},
        )

        LOG.debug(response)
        return response.content
