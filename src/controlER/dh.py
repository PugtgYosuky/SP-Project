"""
Authors:
- Joana Simoes, n.º 2019217013
- Tomas Ferreira, n.º 2019224786
"""

# Importing the libraries needed
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import time


# Diffie-Hellman algorithm
class DH:
    def __init__(self, communication):
        """
        It generates a public key and a private key, and then sends the public key to the other party
        
        :param communication: a class that handles the communication between the two parties
        """
        self.communication = communication
        start_time = time.time()
        # generates the keys
        self.parameters_key = dh.generate_parameters(generator=2, key_size=2048)
        self.private_key = self.parameters_key.generate_private_key()
        self.public_key = self.private_key.public_key()
        end_time = time.time()
        print(f"Generate keys in {round(end_time - start_time)*10**3} ms")
        # sends the public values to the other party
        self.communication.add_value(self.parameters_key.parameter_numbers().p, 'P')
        self.communication.add_value(self.parameters_key.parameter_numbers().g, 'G')
        self.communication.write_bytes(self.public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo), 'DHcontrol')


    def calculate_private_key(self):
        """
        Calculate a shared secret between the two parties
        :return: The common private key or None if an error occurred
        """
        decoded = self.communication.get_bytes('DHdelentture')
        if decoded is None:
            return None
        try:
            other_public_key = load_pem_public_key(decoded)
            algorithm = hashes.SHA256() # TODO: change algorithm
            self.shared_secret = self.private_key.exchange(other_public_key)
            self.common_private_key = HKDF(
                algorithm = algorithm, 
                length=32,
                salt=None, 
                info=b'handshake data',
                backend=default_backend()
            ).derive(self.shared_secret)
            return self.common_private_key
        except:   
            print("Error calculating the private shared key")
            return None

