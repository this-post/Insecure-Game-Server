import azure.functions as func
from Constant import msg_config, server_config
from Security import cert_pinning
from HttpMessageHandling import request_validation, response_handler, response_model

class CERT_PINNING_DTO():
    def __init__(self, key_id: str = None) -> None:
        self.KeyId = key_id

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    if not request_validation.is_valid_json(req, context):
        return response_handler.send_invalid_json_response()
    req_body = req.get_json()
    request_dto = CERT_PINNING_DTO(
        key_id = req_body.get('KeyId')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    sha512_fingerprints = cert_pinning.get_pinned_cert_sha512()
    if not sha512_fingerprints:
        response_dto = response_model.COMMON_RESPONSE_DTO(
            code = msg_config.CERT_GET_URL_ERROR_CODE,
            message = msg_config.CERT_GET_URL_ERROR
        )
        return response_handler.send_response(response_dto, server_config.INTERNAL_ERROR_CODE)
    else:
        return response_handler.send_cert_pinning_response(request_dto.KeyId, sha512_fingerprints)