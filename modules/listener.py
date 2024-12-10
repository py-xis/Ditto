import time
from modules.database import Firebase
from modules.clipboard import Clipboard

class Listener:
    """Listener class for monitoring updates from Firebase."""

    def __init__(self, user: str, clipboard : Clipboard, firebase : Firebase):
        """
        Initialize the Listener with a Firebase instance.
        Args:
            user (str): The user identifier for Firebase operations.
        """
        self.firebase = firebase  # Instance of Firebase class
        self.clipboard = clipboard  # Instance of Clipboard class

    def listen_for_updates(self):
        """
        Listens for updates from Firebase and updates the clipboard.
        Keeps the thread alive to continuously monitor changes.
        """
        print("Listener:listen_for_updates:Starting to listen for updates from Firebase...")
        try:
            # Start listening for updates
            self.firebase.read_from_db(self.clipboard)

        except KeyboardInterrupt:
            print("Listener:listen_for_updates:Stopping listener...")

# # Example Usage
# if __name__ == "__main__":
#     user = "pranav_kulkfrom Encarni"  # Replace with your user identifier
#     listener = Listener(user)
#     listener.listen_for_updates()

#     # Keep the thread alive
#     print("Listening for updates. Press Ctrl+C to stop.")
#     while True:
#         time.sleep(1)