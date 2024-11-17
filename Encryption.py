from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import keywrap
import os


class Encryption(ABC):
    """Abstract Encryption class."""

    @abstractmethod
    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts plaintext and returns ciphertext."""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts ciphertext and returns plaintext."""
        pass

    @abstractmethod
    def get_key(self) -> bytes:
        """Returns the encryption key."""
        pass


class AES256Encryption(Encryption):
    """AES-256 Encryption implementation using cryptography."""

    def __init__(self):
        # Generate a 256-bit key (32 bytes)
        self.key = b' \xa1\xf2\x13\xe1\x07]O\tQ\xdc\x19\x0fZ\xc6V\x80\xb8VL\xa5\x9ca\x012k]\x82a\xc3\xa6\xc7'  # AES-256 requires a 32-byte key
        self.block_size = 128  # Block size for AES is always 128 bits (16 bytes)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts plaintext using AES-256."""
        iv = os.urandom(16)  # Generate a 16-byte IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Apply PKCS7 padding
        padder = PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        # Encrypt the padded data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext  # Prepend IV to the ciphertext

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts ciphertext using AES-256."""
        iv = ciphertext[:16]  # Extract the IV
        actual_ciphertext = ciphertext[16:]  # Extract the actual ciphertext
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt and remove PKCS7 padding
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        unpadder = PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode('utf-8')  # Convert bytes to string

    def get_key(self) -> bytes:
        """Returns the 256-bit encryption key."""
        return self.key


# # Example Usage
# if __name__ == "__main__":
#     aes = AES256Encryption()

#     # Encrypt data
#     plaintext = "This is a secret message."
#     ciphertext = aes.encrypt(plaintext)
#     print("Ciphertext:", ciphertext)

#     # Decrypt data
#     decrypted_text = aes.decrypt(ciphertext)
#     print("Decrypted Text:", decrypted_text)

#     # Get encryption key
#     print("Encryption Key:", aes.get_key())