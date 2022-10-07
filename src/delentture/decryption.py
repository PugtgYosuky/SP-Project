from Crypto.Util import Counter
from Crypto.Cipher import AES
import pandas as pd
from io import StringIO


class Decryption:
    def __init__(self, communication, key):
        self.communication = communication
        self.key = key

    def decrypt(self, filename, counter_size=128):
        iv = self.communication.get_value('iv')
        counter = Counter.new(counter_size, initial_value=iv)    
        aes = AES.new(key=self.key, mode=AES.MODE_CTR, counter=counter)
        ct = self.communication.get_bytes(filename)
        decrypted = aes.decrypt(ct)
        return pd.read_csv(StringIO(decrypted.decode('utf-8')))
