from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Util.number import getRandomNBitInteger
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Random import get_random_bytes

class Encryption:

    def __init__(self, communication, key):
        self.communication = communication
        self.key = key

    def encrypt(self, filename, path, counter_size=128):
        file_path = os.path.join(path, filename)
        iv = getRandomNBitInteger(counter_size)
        self.communication.add_value(iv, 'iv')
        counter = Counter.new(counter_size, initial_value=iv)
        aes = AES.new(self.key, mode=AES.MODE_CTR, counter=counter)
        with open(file_path, 'rb') as file:
            csv_data = file.read()
            encrypted_data = aes.encrypt(csv_data)
            file.close()
        self.communication.write_bytes(encrypted_data, filename.split('.')[0])

    def encrypt_authenticated(self, filename, path):
        # using GCM
        file_path = os.path.join(path, filename)
        # nonce
        nonce = get_random_bytes(12)
        self.communication.write_bytes(nonce, 'nonce')
        aesgcm = AESGCM(self.key)

        with open(file_path, 'rb') as file:
            csv_data = file.read()
            encrypted_data = aesgcm.encrypt(nonce, csv_data, None)
            file.close()

        self.communication.write_bytes(encrypted_data, filename.split('.')[0])








