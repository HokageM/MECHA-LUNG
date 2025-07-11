"""
Encryption utilities for sensitive patient data
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import settings

def generate_key_from_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
    Generate encryption key from password using PBKDF2
    
    Args:
        password: Password to derive key from
        salt: Salt bytes (generated if None)
        
    Returns:
        tuple: (key, salt)
    """
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def get_encryption_key() -> bytes:
    """
    Get or generate encryption key for patient data
    """
    # Use a fixed password for demo (in production, use environment variable)
    password = settings.ENCRYPTION_PASSWORD
    salt = settings.ENCRYPTION_SALT
    
    if not salt:
        # Generate new salt if not exists
        key, salt = generate_key_from_password(password)
        # In production, store salt securely
        print(f"Generated new salt: {base64.b64encode(salt).decode()}")
        return key
    
    # Use existing salt
    key, _ = generate_key_from_password(password, base64.b64decode(salt))
    return key

def encrypt_text(text: str) -> str:
    """
    Encrypt text using Fernet
    
    Args:
        text: Text to encrypt
        
    Returns:
        str: Base64 encoded encrypted text
    """
    if not text:
        return ""
    
    key = get_encryption_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_text(encrypted_text: str) -> str:
    """
    Decrypt text using Fernet
    
    Args:
        encrypted_text: Base64 encoded encrypted text
        
    Returns:
        str: Decrypted text
    """
    if not encrypted_text:
        return ""
    
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        encrypted_bytes = base64.b64decode(encrypted_text.encode())
        decrypted = fernet.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return "[ENCRYPTED]" 