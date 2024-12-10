import base64
import pyperclip
from PIL import Image
import io
from firebase_admin import credentials, firestore, initialize_app
from modules.Encryption import AES256Encryption
from abc import ABC, abstractmethod
from threading import Lock
import os
from modules.clipboard import Clipboard
import time
import platform

class Database(ABC):
    """Abstract Database class."""

    @abstractmethod
    def write_to_db(self, data: str):
        """Writes data to the database."""
        pass

    @abstractmethod
    def read_from_db(self, clipboard):
        """Reads data from the database and updates the clipboard."""
        pass


class Firebase(Database):
    """Firebase class for interacting with Firestore, using AES-256 encryption."""

    _instance = None
    _lock = Lock()  # Thread-safe singleton implementation

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Firebase, cls).__new__(cls)
        return cls._instance

    def __init__(self, user):
        if not hasattr(self, "initialized"):  # Avoid reinitialization in singleton
            self.initialized = True
            # Initialize Firebase admin SDK
            cred = credentials.Certificate("ditto-2d5d7-4124007c9c4f.json")
            initialize_app(cred)
            self.db = firestore.client()
            self.encryption = AES256Encryption()  # Instance of AES256Encryption
            self.user = user
            self.device_name = platform.node()
            self.last_text_from_listener = ""

    def write_to_db(self, data: str):
        """Encrypts and writes data to Firestore."""
        print(f"The key is {self.encryption.get_key().hex()}")
        print(f"The key is {self.encryption.get_key().hex()}")
        try:
            # Encrypt the data
            if(self.last_text_from_listener == data):
                print(f"Database:write_to_db:Ignoring update of {data}")
            else:
                encrypted_data = self.encryption.encrypt(data)

                # Convert ciphertext to base64 for storage in Firestore
                encrypted_data_b64 = encrypted_data.hex()

                # Write the encrypted data to Firestore
                doc_ref = (
                    self.db.collection("clipboard_data")
                    .document(self.user)
                    .collection(self.device_name)
                    .document("clipData")
                )

                doc_ref.set({"content": encrypted_data_b64})
                print(f"Database:write_to_db:{data} successfully written to Firestore.")
        except Exception as e:
            print(f"Database:write_to_db:Error writing to Firestore: {e}")

    # def read_from_db(self, clipboard):
    #     """Sets up listeners for each device in Firestore and updates the clipboard."""
    #     try:
    #         print(f"Database:read_from_db:The key is {self.encryption.get_key()}")
    #         print(f"Database:read_from_db:The Encryption of hello is {self.encryption.encrypt('hello').hex()}")
    #         # Reference to devices
    #         devices_ref = (
    #             self.db.collection("clipboard_data")
    #             .document(self.user)
    #             .collection("devices")
    #             .document("devices")
    #         )
    #         devices_snapshot = devices_ref.get()
    #         devices = devices_snapshot.to_dict()

    #         if not devices:
    #             print("No devices found.")
    #             return

    #         # Set up listeners for all devices except the current device
    #         for device_name in devices:
    #             if devices[device_name] != self.device_name:
    #                 print(f"Database:read_from_db:Setting up listener for device: {devices[device_name]}")
    #                 clip_data_ref = (
    #                     self.db.collection("clipboard_data")
    #                     .document(self.user)
    #                     .collection(devices[device_name])
    #                     .document("clipData")
    #                 )
    #                 clip_data_ref.on_snapshot(self.clip_data_change(clipboard))
    #     except Exception as e:
    #         print(f"Database:read_from_db:Error setting up listeners in Firestore: {e}")

    def read_from_db(self, clipboard):
        """Sets up listeners for each device in Firestore and updates the clipboard."""
        try:
            print(f"Database:read_from_db:The key is {self.encryption.get_key()}")
            print(f"Database:read_from_db:The Encryption of hello is {self.encryption.encrypt('hello').hex()}")
            
            # Listen for changes to the 'devices' document
            self.listen_to_devices(clipboard)

            # Initial setup of listeners
            devices_ref = (
                self.db.collection("clipboard_data")
                .document(self.user)
                .collection("devices")
                .document("devices")
            )
            devices_snapshot = devices_ref.get()
            devices = devices_snapshot.to_dict()

            if not devices:
                print("No devices found.")
                return

            for device_name in devices.values():
                if device_name != self.device_name:
                    print(f"Database:read_from_db:Setting up listener for device: {device_name}")
                    clip_data_ref = (
                        self.db.collection("clipboard_data")
                        .document(self.user)
                        .collection(device_name)
                        .document("clipData")
                    )
                    clip_data_ref.on_snapshot(self.clip_data_change(clipboard))
        except Exception as e:
            print(f"Database:read_from_db:Error setting up listeners in Firestore: {e}")

    def clip_data_change(self, clipboard):
        """Callback for Firestore snapshot changes."""
        def callback(doc_snapshot, changes, read_time):
            for doc in doc_snapshot:
                data = doc.to_dict()
                if not data:
                    continue
                data_type = data.get("dataType", "text")
                encrypted_content = data.get("content", "")

                if not encrypted_content:
                    continue

                try:
                    # Decrypt the data
                    encrypted_data = bytes.fromhex(encrypted_content)
                    content = self.encryption.decrypt(encrypted_data)

                    if data_type == "text":
                        self.last_text_from_listener = content
                        clipboard.write_clipboard(content)
                        print(f"Database:clip_data_change:callback:Text content copied to clipboard: {content}")
                    elif data_type == "image":
                        self.last_text_from_listener = content
                        image_data = base64.b64decode(content)
                        image = Image.open(io.BytesIO(image_data))
                        image.show()  # Display image
                        print("Database:clip_data_change:callback:Image displayed.")
                except Exception as e:
                    print(f"Database:clip_data_change:callback:Error processing data: {e}")

        return callback
    
    def add_new_device(self):
        """
        Adds the current device to the 'devices' document in Firestore.
        The devices are listed sequentially as 'device1', 'device2', etc.
        """
        try:
            # Reference to the 'devices' document
            devices_ref = (
                self.db.collection("clipboard_data")
                .document(self.user)
                .collection("devices")
                .document("devices")
            )

            # Get the current list of devices
            devices_snapshot = devices_ref.get()
            devices = devices_snapshot.to_dict() or {}

            # Check if the current device is already added
            if self.device_name in devices.values():
                print(f"Device '{self.device_name}' is already registered.")
                return

            # Find the next available key (e.g., 'device3')
            device_count = len(devices)
            next_device_key = f"device{device_count + 1}"

            # Add the new device
            devices[next_device_key] = self.device_name
            devices_ref.set(devices)  # Update Firestore with the new device

            print(f"Device '{self.device_name}' added successfully as '{next_device_key}'.")
        except Exception as e:
            print(f"Error adding device: {e}")

    def listen_to_devices(self, clipboard):
        """
        Sets up a listener for the 'devices' document to dynamically update listeners
        when devices are added, removed, or updated.
        """
        try:
            # Reference to the 'devices' document
            devices_ref = (
                self.db.collection("clipboard_data")
                .document(self.user)
                .collection("devices")
                .document("devices")
            )

            # Callback for handling changes in the 'devices' document
            def devices_callback(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    devices = doc.to_dict() or {}

                    print(f"Database:listen_to_devices:Devices updated: {devices}")

                    # Update listeners for other devices
                    for device_key, device_name in devices.items():
                        if device_name != self.device_name:
                            print(f"Database:listen_to_devices:Updating listener for {device_name}")
                            clip_data_ref = (
                                self.db.collection("clipboard_data")
                                .document(self.user)
                                .collection(device_name)
                                .document("clipData")
                            )
                            clip_data_ref.on_snapshot(self.clip_data_change(clipboard))

            # Set up the listener
            devices_ref.on_snapshot(devices_callback)
            print("Database:listen_to_devices:Listener set up for 'devices' document.")
        except Exception as e:
            print(f"Database:listen_to_devices:Error setting up listener: {e}")



# # Example Usage
# if __name__ == "__main__":
#     user = "pranav_kulkarni"
#     firebase = Firebase(user)


#     clipboard = Clipboard()

#     # # Write data to Firebase
#     # firebase.write_to_db("This is a secret message!")

#     # Listen for updates from Firebase
#     firebase.read_from_db(clipboard)

    # print("Listening for changes. Press Ctrl+C to exit.")
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("Exiting...")
    
