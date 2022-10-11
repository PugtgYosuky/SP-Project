# Importing the libraries that are needed for the encryption.
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Util.number import getRandomNBitInteger
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Random import get_random_bytes

# This class is used to encrypt a file using AES in CTR mode or AES-GCM mode
class Encryption:

    def __init__(self, communication, key):
        """
        This function initializes the class with the communication and key parameters
        
        :param communication: The communication object that is used to exchange messages
        :param key: The key to use for the encryption
        """
        self.communication = communication
        self.key = key

    def encrypt(self, filename, path, counter_size=128):
        """
        Encrypts a file using AES in CTR mode (unauthenticated) and sends it
        
        :param filename: The name of the file to be encrypted
        :param path: The path to the file
        :param counter_size: The size of the counter in bits, defaults to 128 (optional)
        """
        # Joining the path and filename together.
        file_path = os.path.join(path, filename)
        #calculate name
        name = filename.split('.')[0]
        # generating iv and send it
        iv = getRandomNBitInteger(counter_size)
        self.communication.add_value(iv, f'iv_{name}')
        # Creating a counter object with the given counter size and initial value.
        counter = Counter.new(counter_size, initial_value=iv)
        # Creating a new AES object with the given key, mode and counter.
        aes = AES.new(self.key, mode=AES.MODE_CTR, counter=counter)
        # Opening the file, reading the data, encrypting it and then closing the file.
        with open(file_path, 'rb') as file:
            csv_data = file.read()
            encrypted_data = aes.encrypt(csv_data)
            file.close()
        # Sending the encrypted data
        self.communication.write_bytes(encrypted_data, name)

    def encrypt_authenticated(self, filename, path):
        """
        Encrypts a file using AES in GCM mode (authenticated) and sends it
        
        :param filename: the name of the file to be encrypted
        :param path: the path to the file
        """
        #calculate name
        name = filename.split('.')[0]
        # Joining the path and filename together.
        file_path = os.path.join(path, filename)
        # The nonce is a random number and sending it
        nonce = get_random_bytes(12)
        self.communication.write_bytes(nonce, f'nonce_{name}')
        # Creating a new AESGCM object with the given key.
        aesgcm = AESGCM(self.key)
        # Opening the file, reading the data, encrypting it and then closing the file.
        with open(file_path, 'rb') as file:
            csv_data = file.read()
            encrypted_data = aesgcm.encrypt(nonce, csv_data, None)
            file.close()

        # Sending the encrypted data
        self.communication.write_bytes(encrypted_data, name)
