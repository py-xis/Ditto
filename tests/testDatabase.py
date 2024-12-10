import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory (containing the 'modules' folder) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.database import Firebase
from modules.clipboard import Clipboard


class TestFirebase(unittest.TestCase):
    @patch("modules.database.credentials.Certificate")
    @patch("modules.database.initialize_app")
    @patch("modules.database.firestore.client")
    def setUp(self, mock_firestore, mock_initialize_app, mock_certificate):
        """Set up Firebase instance with mocked dependencies."""
        self.mock_firestore = mock_firestore
        self.mock_firestore_instance = MagicMock()
        mock_firestore.return_value = self.mock_firestore_instance

        self.user = "test_user"
        self.firebase = Firebase(self.user)
        self.firebase.db = self.mock_firestore_instance

    def test_singleton(self):
        """Test that Firebase follows the Singleton pattern."""
        firebase2 = Firebase(self.user)
        self.assertIs(self.firebase, firebase2)

    @patch("modules.database.AES256Encryption.encrypt")
    def test_write_to_db(self, mock_encrypt):
        """Test writing encrypted data to Firestore."""
        mock_encrypt.return_value = b"encrypted_data"
        self.firebase.write_to_db("Test Data")

        doc_ref = (
            self.mock_firestore_instance.collection.return_value.document.return_value
            .collection.return_value.document.return_value
        )
        doc_ref.set.assert_called_once_with({"content": "656e637279707465645f64617461"})

    @patch("modules.database.AES256Encryption.decrypt")
    def test_clip_data_change(self, mock_decrypt):
        """Test the callback for Firestore snapshot changes."""
        mock_decrypt.return_value = "Decrypted Data"
        clipboard = MagicMock(spec=Clipboard)

        callback = self.firebase.clip_data_change(clipboard)
        doc_snapshot = [MagicMock()]
        doc_snapshot[0].to_dict.return_value = {"content": "656e637279707465645f64617461", "dataType": "text"}

        callback(doc_snapshot, None, None)
        clipboard.write_clipboard.assert_called_once_with("Decrypted Data")

    @patch("modules.database.firestore.DocumentReference.get")
    @patch("modules.database.firestore.DocumentReference.set")
    def test_read_from_db(self, mock_set, mock_get):
        """Test setting up listeners for devices."""
        mock_get.return_value.to_dict.return_value = {"device1": "DeviceA", "device2": "DeviceB"}

        clipboard = MagicMock(spec=Clipboard)
        self.firebase.device_name = "DeviceA"
        self.firebase.read_from_db(clipboard)

        clip_data_ref = self.mock_firestore_instance.collection.return_value.document.return_value.collection.return_value.document.return_value
        clip_data_ref.on_snapshot.assert_called_once()


    @patch("modules.database.firestore.DocumentReference.get")
    @patch("modules.database.firestore.DocumentReference.set")
    def test_add_new_device(self, mock_set, mock_get):
        """Test adding a new device to Firestore."""

        # Mock the `get()` method to return a dictionary of existing devices
        mock_get.return_value.to_dict.return_value = {"device1": "DeviceA", "device2": "DeviceB"}
        
        # Mock the Firestore document reference
        devices_ref = self.mock_firestore_instance.collection.return_value.document.return_value.collection.return_value.document.return_value

        # Ensure the mocked `devices_ref.get()` returns the same mocked data
        devices_ref.get.return_value.to_dict.return_value = {"device1": "DeviceA", "device2": "DeviceB"}

        # Set up a debug print to check the mock's behavior
        print(f"device_ref.get(): {devices_ref.get().to_dict()}")

        # Assign a new device name and add the device
        self.firebase.device_name = "DeviceC"
        self.firebase.add_new_device()

        # Verify the `set` method was called with the correct arguments
        devices_ref.set.assert_called_once_with({"device1": "DeviceA", "device2": "DeviceB", "device3": "DeviceC"})



    @patch("modules.database.firestore.DocumentReference.get")
    @patch("modules.database.firestore.DocumentReference.set")
    def test_add_existing_device(self, mock_set, mock_get):
        """Test that an existing device is not added again."""
        mock_get.return_value.to_dict.return_value = {"device1": "DeviceA", "device2": "DeviceB"}
        devices_ref = self.mock_firestore_instance.collection.return_value.document.return_value.collection.return_value.document.return_value

        self.firebase.device_name = "DeviceB"
        self.firebase.add_new_device()

        mock_set.assert_not_called()


if __name__ == "__main__":
    unittest.main()