from cryptography.fernet import Fernet
import os
from src.soulprint.app.models.db import db
key = os.getenv('ENCRYPTION_KEY')

if key is None:
    key = Fernet.generate_key()
    # Ideally, save this securely elsewhere; for now, keep in memory or .env

cipher_suite = Fernet(key)

def encrypt_message(message: str) -> bytes:
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    return cipher_suite.decrypt(encrypted_message).decode()
