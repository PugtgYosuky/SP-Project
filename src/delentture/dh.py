from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class DH:
    def __init__(self, communication):
        self.communication = communication
        # generate key
        p_key = self.communication.get_value('P_key')
        g_key = self.communication.get_value('G_key')
        self.pn_key = dh.DHParameterNumbers(p_key, g_key)
        self.parameters_key = self.pn_key.parameters()
        self.private_key = self.parameters_key.generate_private_key()
        self.public_key = self.private_key.public_key()
        #write value
        self.communication.write_bytes(self.public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo), 'DHdelenttureKey')
        
        #generate nonce
        p_iv = self.communication.get_value('P_iv')
        g_iv = self.communication.get_value('G_iv')
        self.pn_iv = dh.DHParameterNumbers(p_iv, g_iv)
        self.parameters_iv = self.pn_iv.parameters()
        self.private_iv = self.parameters_iv.generate_private_key()
        self.public_iv = self.private_iv.public_key()
        # write public value
        self.communication.write_bytes(self.public_iv.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo), 'DHDelenttureIV')


    def calculate_private_key(self):
        decoded = self.communication.get_bytes('DHcontrolKey')
        other_public_key = load_pem_public_key(decoded)
        algorithm = hashes.SHA256() # TODO: change algorithm
        if other_public_key:
            self.shared_secret = self.private_key.exchange(other_public_key)
            self.common_private_key = HKDF(
                algorithm = algorithm, 
                length=32,
                salt=None,
                info=b'handshake data',
                backend=default_backend()
            ).derive(self.shared_secret)
            return self.common_private_key
            
        return None

    def calculate_private_iv(self):
        decoded = self.communication.get_bytes('DHcontrolIV')
        other_public_key = load_pem_public_key(decoded)
        algorithm = hashes.SHA256() # TODO: change algorithm
        if other_public_key:
            self.shared_secret_iv = self.private_iv.exchange(other_public_key)
            self.common_private_iv = HKDF(
                algorithm = algorithm, 
                length=32,
                salt=None,
                info=b'handshake data',
                backend=default_backend()
            ).derive(self.shared_secret_iv)
            return self.common_private_iv
            
        return None