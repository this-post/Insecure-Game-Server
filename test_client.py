from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import requests, json, os

# url = 'http://localhost:1337'
url = 'http://localhost:7071'

client_private_key = ec.generate_private_key(ec.SECP521R1())
client_public_key = client_private_key.public_key().public_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ).hex()
# print(client_public_key)
public_key_post = {"publicKey": client_public_key}
# res = requests.post(url + "/getE2eeParams", json=public_key_post)
res = requests.post(url + "/api/KeyExchange", json=public_key_post)
res_json = json.loads(res.text)
server_public_key = res_json['serverPublicKey']
kid = res_json['keyId']
salt = res_json['salt']

public_key_der = serialization.load_der_public_key(bytes.fromhex(server_public_key))
shared_secret = client_private_key.exchange(ec.ECDH(), public_key_der)
derived_key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=bytes.fromhex(salt), iterations=310000).derive(shared_secret)
# print(derived_key.hex())

res = requests.post(url + "/api/GetPinnedCert", json={"keyId": kid})
res_json = json.loads(res.text)
encrypted = res_json['message']
print(res_json)
nonce = bytes.fromhex(encrypted[:12 * 2])
aad = bytes.fromhex(encrypted[-(16 * 2):])
cipher = bytes.fromhex(encrypted.replace(encrypted[:12 * 2], '').replace(encrypted[-(16 * 2):], ''))
# print(aad.hex())
aesgcm = AESGCM(derived_key)
plain = aesgcm.decrypt(nonce, cipher, aad)
print(plain)

aesgcm = AESGCM(derived_key)
nonce = os.urandom(12)
aad = os.urandom(16)
plain = json.dumps({"email": "test@test.com", "password": "testtest"})
enc = aesgcm.encrypt(nonce, plain.encode('utf-8'), aad)
# print('Nonce: ' + nonce.hex())
# print('AAD: ' + aad.hex())
cipher = nonce.hex() + enc.hex() + aad.hex()
res = requests.post(url + "/api/Login", json={"keyId": kid, "data": cipher})
res_json = json.loads(res.text)
encrypted = res_json['message']
nonce = bytes.fromhex(encrypted[:12 * 2])
aad = bytes.fromhex(encrypted[-(16 * 2):])
cipher = bytes.fromhex(encrypted.replace(encrypted[:12 * 2], '').replace(encrypted[-(16 * 2):], ''))
plain = aesgcm.decrypt(nonce, cipher, aad)
# print(plain)