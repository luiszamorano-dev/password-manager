from cryptography.fernet import Fernet

# Esta clave es fija por ahora. Más adelante la protegeremos.
MASTER_KEY = b'Z7xE7ZSc1Wok1Zj8SaPaA4HiOdtMOfIuY4k4TzpTgQY='
fernet = Fernet(MASTER_KEY)

def encrypt_password(plain_password):
    return fernet.encrypt(plain_password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()