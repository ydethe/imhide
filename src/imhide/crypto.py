from cryptography.fernet import Fernet


def generate_key() -> bytes:
    key = Fernet.generate_key()
    return key


def encrypt(raw: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    token = f.encrypt(raw)
    return token


def decrypt(token: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    data = f.decrypt(token)
    return data
