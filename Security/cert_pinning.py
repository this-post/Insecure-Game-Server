from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from Constant import server_config, msg_config
import ssl

def get_pinned_cert_sha512() -> str:
    cert_pem = ssl.get_server_certificate((server_config.PLAYFAB_URL, 443))
    cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())
    sha512fingerprint = cert.fingerprint(hashes.SHA256())
    return sha512fingerprint.hex()
    