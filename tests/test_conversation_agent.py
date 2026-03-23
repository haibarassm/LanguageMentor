import unittest
import tempfile
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from agents.conversation_agent import ConversationAgent


class TestConversationAgent(unittest.TestCase):
    """测试 ConversationAgent"""

    @patch('agents.conversation_agent.ConversationAgent.create_chatbot')
    @patch('agents.agent_base.ChatOllama')
    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_init(self, mock_history, mock_ollama, mock_create):
        """测试初始化"""
        agent = ConversationAgent("test_session")
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.session_id, "test_session")


if __name__ == '__main__':
    unittest.main()
