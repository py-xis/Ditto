import time
from modules.clipboard import Clipboard
from modules.database import Firebase

class Uploader:
    """Uploader class for monitoring clipboard changes and uploading data to Firebase."""

    def __init__(self, user: str, clipboard : Clipboard, firebase : Firebase):
        self.clipboard = clipboard  # Instance of the Clipboard class
        self.firebase = firebase  # Instance of the Firebase class
        self.last_clipboard_content = None  # To track the last clipboard content

    def monitor_clipboard(self):
        """Monitors the clipboard for changes and uploads new content to Firebase."""
        print("Uploader:monitor_clipboard:Starting clipboard monitoring...")
        try:
            while True:
                # Get current clipboard content
                current_content = self.clipboard.read_clipboard()
                
                # Check if the clipboard content has changed
                if current_content != self.last_clipboard_content and (len(current_content) < 100):
                    print(f"Detected clipboard change: {current_content}")
                    self.firebase.write_to_db(current_content)  # Upload to Firebase
                    self.last_clipboard_content = current_content  # Update the last content

                time.sleep(1)  # Poll the clipboard every second
        except KeyboardInterrupt:
            print("Uploader:monitor_clipboard:Clipboard monitoring stopped.")

# # Example Usage
# if __name__ == "__main__":
#     user = "pranav_kulkarni"  # Replace with your user identifier
#     uploader = Uploader(user)
#     uploader.monitor_clipboard()

#     print("Listening for changes. Press Ctrl+C to exit.")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Exiting...")