from cryptography.fernet import Fernet

class TokenManager:
    def __init__(self, key_path):
        self.key_path = key_path
        self.load_key()

    def generate_key(self):
        with open(self.key_path, "wb") as key_file:
            key_file.write(Fernet.generate_key())

    def load_key(self):
        try:
            with open(self.key_path, "rb") as key_file:
                self.key = key_file.read()
        except FileNotFoundError:
            self.generate_key()
            self.load_key()

    def encrypt(self, token):
        cipher_suite = Fernet(self.key)
        encrypted_token = cipher_suite.encrypt(token.encode())
        return encrypted_token

    def decrypt(self, encrypted_token):
        cipher_suite = Fernet(self.key)
        decrypted_token = cipher_suite.decrypt(encrypted_token).decode()
        return decrypted_token
