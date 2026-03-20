import json
import random
from typing import Optional, List
from langchain_core.language_models.chat_models import BaseChatModel

from .base_agent import BaseAgent
from utils.logger import LOG


class ScenarioAgent(BaseAgent):
    """
    场景代理类，负责处理特定场景的对话训练。
    """

    def __init__(self, scenario_name: str, llm: BaseChatModel, session_id: Optional[str] = None):
        """
        Initialize the scenario agent.

        Args:
            scenario_name: Name of the scenario (e.g., "job_interview", "hotel_checkin")
            llm: Language model instance to use for chat
            session_id: Optional session ID for conversation history
        """
        self.scenario_name = scenario_name
        self.intro_file = f"content/intro/{self.name}.json"
        self.intro_messages = self.load_intro()
        super().__init__(llm, session_id)

    @property
    def name(self) -> str:
        """Get the agent name."""
        return self.scenario_name

    @property
    def prompt_file(self) -> str:
        """Get the prompt file path."""
        return f"prompts/{self.name}_prompt.txt"

    def load_intro(self) -> List[str]:
        """
        Load intro messages from JSON file.

        Returns:
            List of intro message strings

        Raises:
            FileNotFoundError: If intro file is not found
            ValueError: If intro file contains invalid JSON
        """
        try:
            with open(self.intro_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Intro file not found: {self.intro_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in intro file: {self.intro_file}")

    def _get_initial_message(self) -> str:
        """
        Get the initial message for a new session.

        Returns:
            Randomly selected initial message from intro messages
        """
        return random.choice(self.intro_messages)
