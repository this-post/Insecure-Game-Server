import azure.functions as func
import json, logging
from Security.aes_gcm import AES_GCM
from Constant import msg_config, server_config
from . import response_model, request_model

def send_response(response_dto: response_model.COMMON_RESPONSE_DTO, http_code: int) -> func.HttpResponse:
    return func.HttpResponse(
                json.dumps(response_dto.__dict__),
                mimetype = server_config.CONTENT_JSON,
                status_code = http_code
            )

def send_common_response(key_id: str, playfab_callback: any) -> func.HttpResponse:
    try:
        enc_alg = AES_GCM(key_id)
    except KeyError:
        return send_invalid_key_id_response()
    response_dto = response_model.COMMON_RESPONSE_DTO()
    if playfab_callback.success:
        enc_msg = enc_alg.aes_encrypt(json.dumps(playfab_callback.success), key_id)
        response_dto.Code = msg_config.FUNC_CALL_SUCCESS_CODE
        response_dto.Message = enc_msg
        return send_response(response_dto, server_config.OK_CODE)
    if playfab_callback.failure:
        enc_msg = enc_alg.aes_encrypt(json.dumps(playfab_callback.failure), key_id)
        response_dto.Code = msg_config.PLAYFAB_ERROR_CODE
        response_dto.Message = enc_msg
        return send_response(response_dto, server_config.OK_CODE)
    return send_unknown_err_response()

def send_cert_pinning_response(key_id: str, sha512_fingerprints_dict: dict) -> func.HttpResponse:
    try:
        enc_alg = AES_GCM(key_id)
    except KeyError:
        return send_invalid_key_id_response()
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.FUNC_CALL_SUCCESS_CODE,
        message = enc_alg.aes_encrypt(json.dumps(sha512_fingerprints_dict), key_id)
    )
    return send_response(response_dto, server_config.OK_CODE)

def send_playfab_get_balance_error() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_GET_BALANCE_ERROR_CODE,
        message = msg_config.PLAYFAB_GET_BALANCE_ERROR
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_get_catalog_error() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_GET_CATALOG_ERROR_CODE,
        message = msg_config.PLAYFAB_GET_CATALOG_ERROR
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_item_exists() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_ITEM_EXISTS_CODE,
        message = msg_config.PLAYFAB_ITEM_EXISTS
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_item_does_not_exist() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_ITEM_DOES_NOT_EXIST_CODE,
        message = msg_config.PLAYFAB_ITEM_DOES_NOT_EXIST
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_get_item_price_error() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_GET_ITEM_PRICE_ERROR_CODE,
        message = msg_config.PLAYFAB_GET_ITEM_PRICE_ERROR
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_insufficient_fund() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_INSUFFICIENT_FUND_CODE,
        message = msg_config.PLAYFAB_INSUFFICIENT_FUND
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_grant_item_fail() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_GRANT_ITEM_FAIL_CODE,
        message = msg_config.PLAYFAB_GRANT_ITEM_FAIL
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_revoke_item_fail() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_REVOKE_ITEM_FAIL_CODE,
        message = msg_config.PLAYFAB_REVOKE_ITEM_FAIL
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_playfab_get_id_fail() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.PLAYFAB_GET_PLAYFAB_ID_ERROR_CODE,
        message = msg_config.PLAYFAB_GET_PLAYFAB_ID_ERROR
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_not_found_response() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.HTTP_REQ_NOT_FOUND_CODE,
        message = msg_config.HTTP_REQ_NOT_FOUND
    )
    return send_response(response_dto, server_config.NOT_FOUND_CODE)

def send_unauth_response() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.HTTP_REQ_UNAUTH_CODE,
        message = msg_config.HTTP_REQ_UNAUTH
    )
    return send_response(response_dto, server_config.UNAUTH_CODE)
    
def send_invalid_key_id_response() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.KEX_GEN_INVALID_KID_CODE,
        message = msg_config.KEX_GEN_INVALID_KID
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_unknown_err_response() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.UNKNOWN_ERROR_CODE,
        message = msg_config.UNKNOWN_ERROR
    )
    return send_response(response_dto, server_config.INTERNAL_ERROR_CODE)

def send_invalid_json_response() -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.HTTP_REQ_IS_NOT_JSON_CODE,
        message = msg_config.HTTP_REQ_IS_NOT_JSON
    )
    return send_response(response_dto, server_config.BAD_REQ_CODE)

def send_missing_params_response(param_key: str) -> func.HttpResponse:
    response_dto = response_model.COMMON_RESPONSE_DTO(
        code = msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
        message = msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = param_key)
    )
    return send_response(response_dto, server_config.BAD_REQ_CODE)