# use the same key pair on signing/key exchange is not recommended, this just for the sake of simplicity, in real App, please use it seperately

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

class SIGNATURE:
    def __init__(self, client_public_key: bytes) -> None:
        self.ClientPublicKey = client_public_key

    # catch cryptography.exceptions.InvalidSignature for invalid signature
    def verify_signature(self, data: bytes, signature: bytes) -> None:
        self.ClientPublicKey.verify(signature, data, ec.ECDSA(hashes.SHA256()))