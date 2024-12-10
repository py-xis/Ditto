import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.clipboard import Clipboard

class TestClipboard(unittest.TestCase):
    def setUp(self):
        """Set up the Clipboard singleton instance."""
        self.clipboard = Clipboard()

    def test_singleton(self):
        """Test that the Clipboard is a singleton."""
        clipboard2 = Clipboard()
        self.assertIs(self.clipboard, clipboard2)

    def test_write_and_read_clipboard(self):
        """Test writing to and reading from the clipboard."""
        test_data = "Test Clipboard Content"
        self.clipboard.write_clipboard(test_data)
        self.assertEqual(self.clipboard.read_clipboard(), test_data)

if __name__ == "__main__":
    unittest.main()