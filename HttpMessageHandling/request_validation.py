import azure.functions as func
import json, logging
from Constant import msg_config
from Security.aes_gcm import AES_GCM

def validate_encrypted_params(req, context) -> tuple[str, str]:
    expected_param_names = ['KeyId', 'Data']
    try:
        req_body = req.get_json()
        logging.info(msg_config.FUNC_CALL_LOG.format(function_name = context.function_name, json_body = str(req_body)))
    except ValueError:
        response = {
            'Code': msg_config.HTTP_REQ_IS_NOT_JSON_CODE,
            'Message': msg_config.HTTP_REQ_IS_NOT_JSON
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
    kid = req_body.get(expected_param_names[0])
    cipher = req_body.get(expected_param_names[1])
    if not kid:
        response = {
            'Code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'Message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = expected_param_names[0])
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
    if not cipher:
        response = {
            'Code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'Message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = expected_param_names[1])
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
    dec_alg = AES_GCM(kid)
    if not dec_alg.is_valid_kid():
        response = {
            'Code': msg_config.KEX_GEN_INVALID_KID_CODE,
            'Message': msg_config.KEX_GEN_INVALID_KID
        }
        return func.HttpResponse(
            json.dumps(response),
            mimetype = "application/json",
            status_code = 500
        )
    data = dec_alg.aes_decrypt(cipher)
    json_data = json.loads(data)
    return json_data, kid

def validate_decrypted_params(dict_of_params) -> None:
    for k, v in dict_of_params:
        if not v or not k:
            response = {
            'Code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'Message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = k)
            }
            return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 400
            )