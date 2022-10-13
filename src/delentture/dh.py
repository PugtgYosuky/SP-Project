from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Diffie-Hellman algorithm
class DH:
    def __init__(self, communication):
        """
        Generates a public and private key with the parameters P, G received
        
        :param communication: Ta class that handles the communication between the two parties
        """
        self.communication = communication
        # generate keys
        p_key = self.communication.get_value('P')
        if p_key is None:
            print("Could not find value P")
            return
        g_key = self.communication.get_value('G')
        if k_key is None:
            print("Could not find value G")
            return
        try:
            self.pn_key = dh.DHParameterNumbers(p_key, g_key)
            self.parameters_key = self.pn_key.parameters()
            self.private_key = self.parameters_key.generate_private_key()
            self.public_key = self.private_key.public_key()
            #send public key
            self.communication.write_bytes(self.public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo), 'DHdelentture')
        except:
            print("Error generating keys")

    def calculate_private_key(self):
        """
        Calculate a shared secret between the two parties
        :return: The common private key or None if an error occurred
        """
        decoded = self.communication.get_bytes('DHcontrol')
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