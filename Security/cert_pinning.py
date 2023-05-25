from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from Constant.server_config import Trusted_URLs
import ssl

def get_pinned_cert_sha512() -> dict:
    try:
        sha512_fingerprint_dict = {}
        sha512_fingerprint_dict['fingerprint'] = []
        for url in Trusted_URLs:
            # url_key = url.name # key
            url_value = url.value
            cert_pem = ssl.get_server_certificate((url_value, 443))
            cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())
            sha512 = cert.fingerprint(hashes.SHA512())
            sha512_fingerprint_dict['fingerprint'].append({'url': url_value, 'sha512': sha512.hex()})
        return sha512_fingerprint_dict
    except:
        return {}