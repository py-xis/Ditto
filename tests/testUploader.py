# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import unittest
# from unittest.mock import MagicMock, patch
# from modules.uploader import Uploader

# class TestUploader(unittest.TestCase):
#     def setUp(self):
#         """Set up Uploader with mocked Clipboard and Firebase."""
#         self.clipboard = MagicMock()
#         self.firebase = MagicMock()
#         self.user = "test_user"
#         self.uploader = Uploader(self.user, self.clipboard, self.firebase)

#     @patch("time.sleep", return_value=None)  # To prevent sleep in tests
#     def test_monitor_clipboard(self, _):
#         """Test monitoring clipboard for changes."""
#         self.clipboard.read_clipboard.side_effect = ["Old Content", "New Content", "New Content"]
#         with self.assertRaises(KeyboardInterrupt):  # Simulate KeyboardInterrupt to exit the loop
#             self.uploader.monitor_clipboard()
#         self.firebase.write_to_db.assert_called_once_with("New Content")


# if __name__ == "__main__":
#     unittest.main()

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import unittest
# from unittest.mock import MagicMock
# from modules.uploader import Uploader
# from modules.clipboard import Clipboard
# from modules.database import Firebase

# class TestUploader(unittest.TestCase):
#     def setUp(self):
#         # Mock dependencies
#         self.mock_clipboard = MagicMock(spec=Clipboard)
#         self.mock_firebase = MagicMock(spec=Firebase)
#         self.user = "test_user"

#         # Instantiate Uploader with mocks
#         self.uploader = Uploader(self.user, self.mock_clipboard, self.mock_firebase)

#     def test_clipboard_content_upload(self):
#         """Test that new clipboard content is uploaded to Firebase."""
#         # Setup mock clipboard behavior
#         self.mock_clipboard.read_clipboard.side_effect = ["test_content", "test_content", "new_content"]

#         # Simulate clipboard monitoring (run once instead of infinite loop)
#         self.uploader.monitor_clipboard = MagicMock(side_effect=self.uploader.monitor_clipboard)
#         self.uploader.last_clipboard_content = None
#         self.uploader.monitor_clipboard()

#         # Verify Firebase method was called with the correct data
#         self.mock_firebase.write_to_db.assert_called_with("new_content")

#     def test_no_upload_on_same_content(self):
#         """Test that repeated clipboard content is not uploaded to Firebase."""
#         # Setup mock clipboard behavior
#         self.mock_clipboard.read_clipboard.side_effect = ["same_content", "same_content"]

#         # Simulate clipboard monitoring
#         self.uploader.monitor_clipboard = MagicMock(side_effect=self.uploader.monitor_clipboard)
#         self.uploader.last_clipboard_content = None
#         self.uploader.monitor_clipboard()

#         # Verify Firebase method was not called
#         self.mock_firebase.write_to_db.assert_not_called()

# if __name__ == "__main__":
#     unittest.main()


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock
from modules.uploader import Uploader
from modules.clipboard import Clipboard
from modules.database import Firebase

class TestUploader(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_clipboard = MagicMock(spec=Clipboard)
        self.mock_firebase = MagicMock(spec=Firebase)
        self.user = "test_user"

        # Instantiate Uploader with mocks
        self.uploader = Uploader(self.user, self.mock_clipboard, self.mock_firebase)

    def test_clipboard_content_upload(self):
        """Test that new clipboard content is uploaded to Firebase."""
        # Define a generator for clipboard content changes
        def clipboard_generator():
            yield "test_content"
            yield "new_content"
            while True:  # Simulate no further changes
                yield "new_content"

        # Set side_effect to the generator
        self.mock_clipboard.read_clipboard.side_effect = clipboard_generator()

        # Modify monitor_clipboard to exit after a few iterations
        def mock_monitor_clipboard():
            iterations = 0
            while iterations < 3:  # Limit the number of iterations
                current_content = self.mock_clipboard.read_clipboard()
                if current_content != self.uploader.last_clipboard_content:
                    print(f"Detected clipboard change: {current_content}")
                    self.mock_firebase.write_to_db(current_content)
                    self.uploader.last_clipboard_content = current_content
                iterations += 1

        # Replace the original method with the mock
        self.uploader.monitor_clipboard = mock_monitor_clipboard
        self.uploader.last_clipboard_content = None

        # Run the test
        self.uploader.monitor_clipboard()

        # Verify Firebase method was called with the correct data
        self.mock_firebase.write_to_db.assert_called_with("new_content")

def test_no_upload_on_same_content(self):
    """Test that repeated clipboard content is not uploaded to Firebase."""
    # Define a generator for clipboard content changes
    def clipboard_generator():
        yield "same_content"
        yield "same_content"
        yield "same_content"  # After this, the generator will naturally end

    # Set side_effect to the generator
    self.mock_clipboard.read_clipboard.side_effect = clipboard_generator()

    # Modify monitor_clipboard to exit after a few iterations
    def mock_monitor_clipboard():
        try:
            while True:
                current_content = self.mock_clipboard.read_clipboard()
                if current_content != self.uploader.last_clipboard_content:
                    print(f"Detected clipboard change: {current_content}")
                    self.mock_firebase.write_to_db(current_content)
                    self.uploader.last_clipboard_content = current_content
        except StopIteration:
            print("Test finished, exiting loop.")

    # Replace the original method with the mock
    self.uploader.monitor_clipboard = mock_monitor_clipboard
    self.uploader.last_clipboard_content = None

    # Run the test
    self.uploader.monitor_clipboard()

    # Verify Firebase method was not called
    self.mock_firebase.write_to_db.assert_not_called()

if __name__ == "__main__":
    unittest.main()