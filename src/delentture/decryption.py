# Importing the libraries that are needed for the decryption
from Crypto.Util import Counter
from Crypto.Cipher import AES
import pandas as pd
from io import StringIO
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


#This class is used to decrypt a file using AES in CTR mode or AES-GCM mode
class Decryption:
    def __init__(self, communication, key):
        """
        This function initializes the class with the communication and key parameters
        
        :param communication: The communication object that is used to receive data
        :param key: The key to use for the decryption
        """
        self.communication = communication
        self.key = key

    def decrypt(self, filename, counter_size=128):
        """
        Decrypts a file using AES in CTR mode (unauthenticated)
        
        :param filename: the name of the file to be decrypted
        :param counter_size: The size of the counter in bits. The default is 128 bits, defaults to 128
        (optional)
        :return: A pandas dataframe
        """
        # Reading the iv used to encrypt the file
        iv = self.communication.get_value(f'iv_{filename}')
        # Creating a new counter object with the specified counter size and initial value.
        counter = Counter.new(counter_size, initial_value=iv)    
        # Creating a new AES object with the specified key, mode and counter.
        aes = AES.new(key=self.key, mode=AES.MODE_CTR, counter=counter)
        # Getting the bytes of the file that is to be decrypted.
        ct = self.communication.get_bytes(filename)
        # Decrypting the ciphertext using the AES object.
        decrypted = aes.decrypt(ct)
        # Converting the decrypted bytes to a pandas dataframe.
        return pd.read_csv(StringIO(decrypted.decode('utf-8')))

    def decrypt_authenticated(self, filename):
        """
        Decrypts a file using AES in GCM mode (authenticated)
        
        :param filename: The name of the file to be decrypted
        :return: A pandas dataframe
        """
        # Getting the nonce from the communication object.
        nonce = self.communication.get_bytes(f'nonce_{filename}')
        # Getting the bytes of the file that is to be decrypted.
        ct = self.communication.get_bytes(filename)
        try:
            # Creating a new AESGCM object with the specified key.
            aesgcm = AESGCM(self.key)
            # Decrypting the ciphertext using the AESGCM
            decrypted = aesgcm.decrypt(nonce, ct, None)
            # Converting the decrypted bytes to a pandas dataframe.
            return pd.read_csv(StringIO(decrypted.decode('utf-8')))
            
        except:
            print("Error")
            return None
