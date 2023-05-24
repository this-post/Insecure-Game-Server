from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Constant import server_config
import os, redis

class AES_GCM:
    def __init__(self, kid) -> None:
        if server_config.IS_TESTING_ENV_REDIS:
            self._redis = redis.Redis(
                host = 'localhost',
                port = server_config.REDIS_NON_SSL_PORT,
                # decode_responses = True -> this will automatically decode binary to ASCII
            )
        else:
            self._redis = redis.Redis(
                host = server_config.REDIS_HOST,
                port = server_config.REDIS_SSL_PORT,
                ssl = True,
                ssl_cert_reqs = "none",
                password = server_config.REDIS_PWD,
                # decode_responses = True -> this will automatically decode binary to ASCII
            )
        self.kid = kid
    
    def aes_encrypt(self, plain) -> str:
        session_key = self._redis.get(self.kid)
        nonce = os.urandom(16)
        aad = os.urandom(16)
        aesgcm = AESGCM(session_key)
        cipher = aesgcm.encrypt(nonce, plain.encode('utf-8'), aad)
        return nonce.hex() + cipher.hex() + aad.hex() # 16 bytes of nonce + cipher + 16 bytes of AAD

    def aes_decrypt(self, cipher) -> str:
        session_key = self._redis.get(self.kid)
        nonce = bytes.fromhex(cipher[:16 * 2])
        aad = bytes.fromhex(cipher[-(16 * 2):])
        cipher = bytes.fromhex(cipher.replace(cipher[:16 * 2], '').replace(cipher[-(16 * 2):], ''))
        aesgcm = AESGCM(session_key)
        plain = aesgcm.decrypt(nonce, cipher, aad)
        return plain
    
    def is_valid_kid(self) -> bool:
        if self._redis.get(self.kid):
            return True
        else:
            return False