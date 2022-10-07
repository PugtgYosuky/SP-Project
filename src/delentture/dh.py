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
        p_key = self.communication.get_value('P')
        g_key = self.communication.get_value('G')
        self.pn_key = dh.DHParameterNumbers(p_key, g_key)
        self.parameters_key = self.pn_key.parameters()
        self.private_key = self.parameters_key.generate_private_key()
        self.public_key = self.private_key.public_key()
        #write value
        self.communication.write_bytes(self.public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo), 'DHdelentture')


    def calculate_private_key(self):
        decoded = self.communication.get_bytes('DHcontrol')
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
