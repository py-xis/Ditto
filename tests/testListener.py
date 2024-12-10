import unittest
from unittest.mock import MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.listener import Listener

class TestListener(unittest.TestCase):
    def setUp(self):
        """Set up Listener with mocked Clipboard and Firebase."""
        self.clipboard = MagicMock()
        self.firebase = MagicMock()
        self.user = "test_user"
        self.listener = Listener(self.user, self.clipboard, self.firebase)

    def test_listen_for_updates(self):
        """Test that the Listener calls Firebase's read_from_db."""
        self.listener.listen_for_updates()
        self.firebase.read_from_db.assert_called_with(self.clipboard)

if __name__ == "__main__":
    unittest.main()