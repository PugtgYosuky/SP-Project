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
        self.parameters_key = dh.generate_parameters(generator=2, key_size=2048)
        self.private_key = self.parameters_key.generate_private_key()
        self.public_key = self.private_key.public_key()
        # write values
        self.communication.add_value('P', self.parameters_key.parameter_numbers().p)
        self.communication.add_value('G', self.parameters_key.parameter_numbers().g)
        self.communication.write_bytes(self.public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo), 'DHcontrol')


    def calculate_private_key(self):
        decoded = self.communication.get_bytes('DHdelentture')
        other_public_key = load_pem_public_key(decoded)
        algorithm = hashes.SHA256() # TODO: change algorithm
        if other_public_key:
            self.shared_secret = self.private_key.exchange(other_public_key)
            self.common_private_key = HKDF(
                algorithm = algorithm, 
                length=32,
                salt=None, 
                info=b'handshake data', # ! o que é suposto ser aqui
                backend=default_backend()
            ).derive(self.shared_secret)
            return self.common_private_key   
        return None

