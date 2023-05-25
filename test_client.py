from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
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
msg_json = json.loads(res_json['message'])
server_public_key = msg_json['serverPublicKey']
kid = msg_json['kid']
salt = msg_json['salt']

public_key_der = serialization.load_der_public_key(bytes.fromhex(server_public_key))
shared_secret = client_private_key.exchange(ec.ECDH(), public_key_der)
derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=bytes.fromhex(salt), info=b'handshake data').derive(shared_secret)
# print(derived_key.hex())

res = requests.post(url + "/api/GetPinnedCert", json={"kid": kid})
res_json = json.loads(res.text)
encrypted = res_json['message']
# print(encrypted)
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
res = requests.post(url + "/api/Login", json={"kid": kid, "data": cipher})
res_json = json.loads(res.text)
encrypted = res_json['message']
nonce = bytes.fromhex(encrypted[:12 * 2])
aad = bytes.fromhex(encrypted[-(16 * 2):])
cipher = bytes.fromhex(encrypted.replace(encrypted[:12 * 2], '').replace(encrypted[-(16 * 2):], ''))
plain = aesgcm.decrypt(nonce, cipher, aad)
print(plain)