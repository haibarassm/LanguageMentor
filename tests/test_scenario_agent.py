import unittest
import tempfile
import os
import json
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from agents.scenario_agent import ScenarioAgent


class TestScenarioAgent(unittest.TestCase):
    """测试 ScenarioAgent"""

    @patch('agents.scenario_agent.ScenarioAgent.create_chatbot')
    @patch('agents.agent_base.ChatOllama')
    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_init(self, mock_history, mock_ollama, mock_create):
        """测试初始化"""
        agent = ScenarioAgent("job_interview")
        self.assertEqual(agent.name, "job_interview")


if __name__ == '__main__':
    unittest.main()
