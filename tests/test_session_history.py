import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from agents.session_history import get_session_history, store


class TestSessionHistory(unittest.TestCase):
    """测试会话历史"""

    def setUp(self):
        store.clear()

    def tearDown(self):
        store.clear()

    def test_get_session_history(self):
        """测试获取会话历史"""
        history = get_session_history("test_session")
        self.assertIsNotNone(history)
        self.assertIn("test_session", store)


if __name__ == '__main__':
    unittest.main()
