import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.Encryption import AES256Encryption

class TestAES256Encryption(unittest.TestCase):
    def setUp(self):
        """Set up the AES256Encryption instance."""
        self.encryption = AES256Encryption()

    def test_encrypt_and_decrypt(self):
        """Test encrypting and decrypting data."""
        plaintext = "Secret Message"
        ciphertext = self.encryption.encrypt(plaintext)
        decrypted_text = self.encryption.decrypt(ciphertext)
        self.assertEqual(decrypted_text, plaintext)

    def test_key(self):
        """Test getting the encryption key."""
        self.assertEqual(len(self.encryption.get_key()), 32)

if __name__ == "__main__":
    unittest.main()