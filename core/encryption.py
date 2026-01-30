from cryptography.fernet import Fernet
import os
import sys

# Define path for key file
# In a real deployed app, this should be in AppData or ~/.tuvi-app/
# For portable app, putting it next to main.py is acceptable but ensure it's gitignored.
KEY_FILE = "secret.key"

class EncryptionManager:
    _key = None
    _cipher = None

    @classmethod
    def _load_key(cls):
        if cls._key:
            return

        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "rb") as key_file:
                cls._key = key_file.read()
        else:
            cls._key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as key_file:
                key_file.write(cls._key)
        
        cls._cipher = Fernet(cls._key)

    @classmethod
    def encrypt(cls, text: str) -> str:
        """Encrypts a string and returns a hex or base64 string."""
        if not text:
            return ""
        cls._load_key()
        encrypted_bytes = cls._cipher.encrypt(text.encode("utf-8"))
        return encrypted_bytes.decode("utf-8")

    @classmethod
    def decrypt(cls, encrypted_text: str) -> str:
        """Decrypts a string."""
        if not encrypted_text:
            return ""
        cls._load_key()
        try:
            decrypted_bytes = cls._cipher.decrypt(encrypted_text.encode("utf-8"))
            return decrypted_bytes.decode("utf-8")
        except Exception:
            # If decryption fails (e.g. key changed or invalid data), return original or empty
            # Return empty to be safe and force re-entry
            return ""
