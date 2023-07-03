import azure.functions as func
import json, logging
from Security.aes_gcm import AES_GCM
from Constant import msg_config

def send_response(kid, playfab_callback) -> func.HttpResponse:
    enc_alg = AES_GCM(kid)
    if playfab_callback.success:
        enc_msg = enc_alg.aes_encrypt(json.dumps(playfab_callback.success))
        response = {
            'Code': msg_config.FUNC_CALL_SUCCESS_CODE,
            'Message': enc_msg
        }
        return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 200
            )
    if playfab_callback.failure:
        enc_msg = enc_alg.aes_encrypt(json.dumps(playfab_callback.failure))
        response = {
            'Code': msg_config.PLAYFAB_ERROR_CODE,
            'Message': enc_msg
        }
        return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 200
            )
    response = {
        'Code': msg_config.UNKNOWN_ERROR_CODE,
        'Message': msg_config.UNKNOWN_ERROR
    }
    return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 500
            )