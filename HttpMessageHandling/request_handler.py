import json
from Security.aes_gcm import AES_GCM
from . import request_model

def decrypt(request_dto: request_model.COMMON_REQUEST_DTO) -> dict:
    try:
        dec_alg = AES_GCM(request_dto.KeyId)
    except KeyError:
        return {}
    data = dec_alg.aes_decrypt(request_dto.Data)
    json_data = json.loads(data)
    return json_data