import logging, json
import azure.functions as func
from Constant import msg_config
from PlayFabUtil.authen import AUTHEN
from Security.aes_gcm import AES_GCM

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    expected_param_names = ['keyId', 'data']
    try:
        req_body = req.get_json()
        logging.info(msg_config.FUNC_CALL_LOG.format(function_name = context.function_name, json_body = str(req_body)))
    except ValueError:
        response = {
            'code': msg_config.HTTP_REQ_IS_NOT_JSON_CODE,
            'message': msg_config.HTTP_REQ_IS_NOT_JSON
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
            'code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = expected_param_names[0])
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
    if not cipher:
        response = {
            'code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = expected_param_names[1])
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
    dec_alg = AES_GCM(kid)
    if not dec_alg.is_valid_kid():
        response = {
            'code': msg_config.KEX_GEN_INVALID_KID_CODE,
            'message': msg_config.KEX_GEN_INVALID_KID
        }
        return func.HttpResponse(
            json.dumps(response),
            mimetype = "application/json",
            status_code = 500
        )
    data = dec_alg.aes_decrypt(cipher)
    json_data = json.loads(data)
    email = json_data.get('email')
    passwd = json_data.get('password')
    if not email:
        response = {
            'code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = 'email')
        }
        return func.HttpResponse(
            json.dumps(response),
            mimetype = "application/json",
            status_code = 400
        )
    if not passwd:
        response = {
            'code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = 'password')
        }
        return func.HttpResponse(
            json.dumps(response),
            mimetype = "application/json",
            status_code = 400
        )
    playfab_auth_req = {
        'Email': email,
        'Password': passwd
    }
    playfab_auth = AUTHEN()
    playfab_auth.login_with_email(playfab_auth_req)
    enc_alg = AES_GCM(kid)
    if playfab_auth.success:
        # logging.info(playfab_auth.success)
        payload = {
            'result': playfab_auth.success
        }
        enc_msg = enc_alg.aes_encrypt(json.dumps(payload))
        response = {
            'code': msg_config.FUNC_CALL_SUCCESS_CODE,
            'message': enc_msg
        }
        return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 200
            )
    if playfab_auth.failure:
        # logging.info(playfab_auth.failure)
        payload = {
            'result': playfab_auth.failure
        }
        enc_msg = enc_alg.aes_encrypt(json.dumps(payload))
        response = {
            'code': msg_config.FUNC_CALL_SUCCESS_CODE,
            'message': enc_msg
        }
        return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 200
            )
    response = {
        'code': msg_config.UNKNOWN_ERROR_CODE,
        'message': msg_config.UNKNOWN_ERROR
    }
    return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 500
            )
