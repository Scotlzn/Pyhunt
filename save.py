from cryptography.fernet import Fernet
from support import save_json, load_json

class SaveManager:
    def get_fernet_key(self):
        # key = Fernet.generate_key()
        key = b'NlGX1nBydU7-YO8GnJXnYeJNQ5N4hUqoobVKRMhsWjY='
        fernet = Fernet(key)
        return fernet

    def encrypt_data(self, data):
        fernet = self.get_fernet_key()
        byte_data = bytes(data, encoding='utf-8')
        encrypted = fernet.encrypt(byte_data)
        return str(encrypted)

    def decrypt_data(self, data):
        fernet = self.get_fernet_key()
        byte_string = data.split("'")[1]
        byte_data = bytes(byte_string, encoding='utf-8')
        string_data = fernet.decrypt(byte_data)
        return int(str(string_data).split("'")[1])

    def save(self, locations, data):
        output = {}
        for i, variable in enumerate(data):
            output[locations[i]] = self.encrypt_data(str(variable))
        save_json('data/savedata', output)

    def load(self):
        savedata = load_json('data/savedata')
        output = []
        for data in savedata.values():
            output.append(self.decrypt_data(data))
        return output
