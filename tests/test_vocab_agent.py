import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from agents.vocab_agent import VocabAgent


class TestVocabAgent(unittest.TestCase):
    """测试 VocabAgent"""

    @patch('agents.vocab_agent.VocabAgent.create_chatbot')
    @patch('agents.agent_base.ChatOllama')
    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_init(self, mock_history, mock_ollama, mock_create):
        """测试初始化"""
        agent = VocabAgent("test_session")
        self.assertEqual(agent.name, "vocab_study")


if __name__ == '__main__':
    unittest.main()
