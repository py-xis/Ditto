import pyperclip
from threading import Lock

class Clipboard:
    _instance = None
    _lock = Lock() 

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Clipboard, cls).__new__(cls)
        return cls._instance

    def read_clipboard(self):
        """Reads the current content of the clipboard."""
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Clipboard : Error reading clipboard: {e}")
            return None

    def write_clipboard(self, data):
        """Writes content to the clipboard."""
        try:
            pyperclip.copy(data)
        except Exception as e:
            print(f"Clipboard : Error writing to clipboard: {e}")

# # Example Usage
# if __name__ == "__main__":
#     clipboard1 = Clipboard()
#     clipboard2 = Clipboard()

#     # Verify singleton instance
#     print(clipboard1 is clipboard2)  # Output: True

#     # Use the Clipboard instance
#     clipboard1.write_clipboard("Singleton Clipboard Content")
#     print(clipboard2.read_clipboard())  # Output: Singleton Clipboard Content