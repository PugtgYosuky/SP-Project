from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import os
from cryptography.hazmat.primitives import hashes


class SignVerifyDocument:
    def __init__(self, entity, other_entity, communication):
        self.entity = entity
        self.other_entity = other_entity
        self.communication = communication
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        pem_key = self.public_key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
        self.communication.write_bytes(pem_key, f'rsa_public_key_{self.entity}')

    def sign_document(self, data_to_sign):
        padding_obj = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
        algorithm = algorithm=hashes.SHA256()
        signature = self.private_key.sign(data_to_sign, padding_obj, algorithm=algorithm)
        return signature

    def verify_document(self, data_to_verify, message):
        other_pem_key = self.communication.get_bytes(f'rsa_public_key_{self.other_entity}')
        other_public_key = load_pem_public_key(other_pem_key)
        try:
            padding_obj = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
            algorithm = algorithm=hashes.SHA256()
            other_public_key.verify(data_to_verify, message, padding=padding_obj, algorithm=algorithm)
            return True
        except:
            return False