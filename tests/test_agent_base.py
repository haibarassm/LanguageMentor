import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from agents.agent_base import AgentBase


class TestAgentBase(unittest.TestCase):
    """测试 AgentBase 基本功能"""

    def setUp(self):
        self.temp_prompt = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.temp_prompt.write("Test prompt")
        self.temp_prompt.close()

    def tearDown(self):
        if os.path.exists(self.temp_prompt.name):
            os.remove(self.temp_prompt.name)

    @patch('agents.agent_base.ChatOllama')
    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_init(self, mock_history, mock_ollama):
        """测试初始化"""
        agent = AgentBase("test", self.temp_prompt.name)
        self.assertEqual(agent.name, "test")
        self.assertEqual(agent.prompt, "Test prompt")

    def test_load_prompt_file_not_found(self):
        """测试文件不存在"""
        with self.assertRaises(FileNotFoundError):
            AgentBase("test", "nonexistent.txt")


if __name__ == '__main__':
    unittest.main()
