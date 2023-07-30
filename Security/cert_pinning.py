from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from Constant.server_config import TRUSTED_URLS
import ssl

def get_pinned_cert_sha512() -> dict:
    try:
        sha256_fingerprint_dict = {}
        sha256_fingerprint_dict['Fingerprint'] = []
        for url in TRUSTED_URLS:
            # url_key = url.name # key
            url_value = url.value
            cert_pem = ssl.get_server_certificate((url_value, 443))
            cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())
            sha256 = cert.fingerprint(hashes.SHA256())
            sha256_fingerprint_dict['Fingerprint'].append({'Url': url_value, 'Sha256': sha256.hex()})
        return sha256_fingerprint_dict
    except:
        return {}