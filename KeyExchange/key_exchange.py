import azure.functions as func
from Security.key_agreement import KEY_AGREEMENT
from Constant import msg_config, server_config
from HttpMessageHandling import request_validation, response_handler, response_model

class KEX_REQUEST_DTO():
    def __init__(self, public_key: str = None) -> None:
        self.PublicKey = public_key

class KEX_RESPONSE_DTO():
    def __init__(self, code: int = None, key_id: str = None, salt: str = None, server_public_key: str = None) -> None:
        self.Code = code
        self.KeyId = key_id
        self.Salt = salt
        self.ServerPublicKey = server_public_key

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    if not request_validation.is_valid_json(req, context):
        return response_handler.send_invalid_json_response()
    req_body = req.get_json()
    request_dto = KEX_REQUEST_DTO(
        public_key = req_body.get('PublicKey')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    key_exchange_alg = KEY_AGREEMENT()
    is_success_kex, kex_result = key_exchange_alg.key_exchange(request_dto.PublicKey)
    if not is_success_kex:
        response_dto = response_model.COMMON_RESPONSE_DTO(
            code = msg_config.KEX_GEN_FAILED_CODE,
            message = msg_config.KEX_GEN_FAILED
        )
        return response_handler.send_response(response_dto, server_config.INTERNAL_ERROR_CODE)
    else:
        response_dto = KEX_RESPONSE_DTO(
            code = msg_config.FUNC_CALL_SUCCESS_CODE,
            key_id = kex_result['KeyId'],
            salt = kex_result['Salt'],
            server_public_key = kex_result['ServerPublicKey']
        )
        return response_handler.send_response(response_dto, server_config.OK_CODE)