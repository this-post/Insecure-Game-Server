import logging, json
import azure.functions as func
from Constant import msg_config
from Security.aes_gcm import AES_GCM
from Security import cert_pinning

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    expected_param_name = 'kid'
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
    kid = req_body.get(expected_param_name)
    if kid:
        enc_alg = AES_GCM(kid)
        if enc_alg.is_valid_kid():
            sha512_fingerprints = cert_pinning.get_pinned_cert_sha512()
            if not sha512_fingerprints:
                response = {
                    'code': msg_config.CERT_GET_URL_ERROR_CODE,
                    'message': msg_config.CERT_GET_URL_ERROR
                }
                return func.HttpResponse(
                    json.dumps(response),
                    mimetype = "application/json",
                    status_code = 500
                )
            payload = {
                'result': sha512_fingerprints
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
        else:
            response = {
                'code': msg_config.KEX_GEN_INVALID_KID_CODE,
                'message': msg_config.KEX_GEN_INVALID_KID
            }
            return func.HttpResponse(
                json.dumps(response),
                mimetype = "application/json",
                status_code = 500
            )
    else:
        response = {
            'code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = expected_param_name)
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
