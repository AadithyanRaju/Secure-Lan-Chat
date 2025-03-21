from Crypto.Cipher import AES
import base64
import os

SECRET_KEY = b"16charsecretkey!"  # 16, 24, or 32 bytes key

def pad(text):
    return text + (16 - len(text) % 16) * chr(16 - len(text) % 16)

def unpad(text):
    return text[:-ord(text[-1])]

def encrypt_message(message):
    """Encrypts a message with AES"""
    iv = os.urandom(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message).encode())
    return base64.b64encode(iv + encrypted).decode()

def decrypt_message(encrypted_message):
    """Decrypts an AES-encrypted message"""
    raw = base64.b64decode(encrypted_message)
    iv = raw[:16]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(raw[16:]).decode())

# Test Encryption
if __name__ == "__main__":
    msg = "Hello Secure Chat!"
    enc = encrypt_message(msg)
    print("Encrypted:", enc)
    print("Decrypted:", decrypt_message(enc))
