from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Util.number import getRandomNBitInteger
import os

class Encryption:

    def __init__(self, communication, key):
        self.communication = communication
        self.key = key

    def encrypt(self, filename, path, counter_size=128):
        file_path = os.path.join(path, filename)
        iv = getRandomNBitInteger(counter_size)
        self.communication.add_value('iv', iv)
        counter = Counter.new(counter_size, initial_value=iv)
        aes = AES.new(self.key, mode=AES.MODE_CTR, counter=counter)
        with open(file_path, 'rb') as file:
            csv_data = file.read()
            encrypted_data = aes.encrypt(csv_data)
            file.close()
        self.communication.write_bytes(encrypted_data, filename.split('.')[0])


