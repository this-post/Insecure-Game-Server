from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import UnsupportedAlgorithm
from Constant import msg_config, server_config
import uuid, os, redis, logging

class KEX_RESPONSE_DTO:
    def __init__(self, key_id: str = None, salt: str = None, server_public_key: str = None) -> None:
        self.KeyId = key_id
        self.Salt = salt
        self.ServerPublicKey = server_public_key

class KEY_AGREEMENT:
    def __init__(self) -> None:
        if server_config.IS_TESTING_ENV_REDIS:
            self._redis = redis.Redis(
                host = 'localhost',
                port = server_config.REDIS_NON_SSL_PORT,
                decode_responses = True
            )
        else:
            self._redis = redis.Redis(
                host = server_config.REDIS_HOST,
                port = server_config.REDIS_SSL_PORT,
                ssl = True,
                ssl_cert_reqs = "none",
                password = server_config.REDIS_PWD,
                decode_responses = True
            )
        f = open(server_config.PRIV_KEY_PATH, 'r')
        f_content = f.read()
        self.serv_priv_key = serialization.load_pem_private_key(f_content.encode('utf-8'), password = None)
        f.close()

    def get_shared_secret(self, pub_key) -> bytes:
        client_pub_key_der = serialization.load_der_public_key(bytes.fromhex(pub_key))
        # https://github.com/cose-wg/cose-issues/issues/3
        return self.serv_priv_key.exchange(ec.ECDH(), client_pub_key_der) # this always keep the leading zero as it's convert to Hex, and will incompatible with C# BoucyCastle

    def get_shared_secret_kdf(self, _salt, shared_secret) -> bytes:
        return PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = _salt,
            iterations = 310000
        ).derive(shared_secret)

    def generate_kid(self, session_key) -> str:
        key_id = str(uuid.uuid4())
        self._redis.set(key_id, session_key)
        return key_id

    def key_exchange(self, client_pub_key) -> tuple[bool, dict]:
        try:
            # client_pub_key_der = serialization.load_der_public_key(bytes.fromhex(client_pub_key))
            _salt = os.urandom(16)
            shared_secret = self.get_shared_secret(client_pub_key)
            logging.info('Shared secret: ' + shared_secret.hex())
            session_key = self.get_shared_secret_kdf(_salt, shared_secret)
            logging.info('Session key: ' + session_key.hex())
            _key_id = self.generate_kid(session_key)
            kex_result = KEX_RESPONSE_DTO(
                key_id = _key_id,
                salt = _salt.hex(),
                server_public_key = self.serv_priv_key.public_key().public_bytes(
                    encoding = serialization.Encoding.DER,
                    format = serialization.PublicFormat.SubjectPublicKeyInfo
                ).hex()
            )
            return (True, kex_result.__dict__)
        except ValueError:
            return (False, msg_config.KEX_INVALID_DER)
        except UnsupportedAlgorithm:
            return (False, msg_config.KEX_INVALID_ALG)