from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Constant import msg_config, server_config
import os, redis, logging

class AES_GCM:
    def __init__(self, key_id: str) -> None:
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
        if self._redis.get(key_id):
            self.key_id = key_id
        else:
            raise KeyError(msg_config.KEX_GEN_INVALID_KID)
    
    def aes_encrypt(self, plain: str, key_id: str) -> str:
        session_key = self._redis.get(self.key_id)
        nonce = os.urandom(12)
        # aad = os.urandom(16)
        aad = key_id.encode('utf-8')
        aesgcm = AESGCM(session_key)
        cipher = aesgcm.encrypt(nonce, plain.encode('utf-8'), aad)
        # logging.info('Nonce: ' + nonce.hex())
        # logging.info('AAD: ' + aad.hex())
        # logging.info('Cipher: ' + cipher.hex())
        # return nonce.hex() + cipher.hex() + aad.hex() # 12 bytes of nonce + cipher + 16 bytes of AAD
        return nonce.hex() + cipher.hex()

    def aes_decrypt(self, cipher: str) -> str:
        session_key = self._redis.get(self.key_id)
        nonce = bytes.fromhex(cipher[:12 * 2])
        # aad = bytes.fromhex(cipher[-(16 * 2):])
        aad = self.key_id.encode('utf-8')
        # cipher = bytes.fromhex(cipher.replace(cipher[:12 * 2], '').replace(cipher[-(16 * 2):], ''))
        cipher = bytes.fromhex(cipher.replace(cipher[:12 * 2], ''))
        # logging.info('Nonce: ' + nonce.hex())
        # logging.info('Aad: ' + aad.hex())
        # logging.info('Cipher: ' + cipher.hex())
        aesgcm = AESGCM(session_key)
        plain = aesgcm.decrypt(nonce, cipher, aad)
        return plain
    
    # def is_valid_kid(self, key_id) -> bool:
    #     if self._redis.get(key_id):
    #         return True
    #     else:
    #         return False