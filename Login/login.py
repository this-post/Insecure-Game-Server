import logging, json
import azure.functions as func
from Constant import msg_config
from PlayFabUtil.authen import AUTHEN
from Security.aes_gcm import AES_GCM

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
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
    email = json_data.get('Email')
    passwd = json_data.get('Password')
    if not email:
        response = {
            'Code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'Message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = 'Email')
        }
        return func.HttpResponse(
            json.dumps(response),
            mimetype = "application/json",
            status_code = 400
        )
    if not passwd:
        response = {
            'Code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'Message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = 'Password')
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
        # payload = {
        #     'result': playfab_auth.success
        # }
        enc_msg = enc_alg.aes_encrypt(json.dumps(playfab_auth.success))
        response = {
            'Code': msg_config.FUNC_CALL_SUCCESS_CODE,
            'Message': enc_msg
        }
        return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 200
            )
    if playfab_auth.failure:
        # logging.info(playfab_auth.failure)
        # payload = {
        #     'result': playfab_auth.failure
        # }
        enc_msg = enc_alg.aes_encrypt(json.dumps(playfab_auth.failure))
        response = {
            'Code': msg_config.FUNC_CALL_SUCCESS_CODE,
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
