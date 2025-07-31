from cryptography.fernet import Fernet
import os

# Load or generate encryption key (keep this secret!)
KEY = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(KEY)

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

