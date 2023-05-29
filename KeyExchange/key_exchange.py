import logging, json
import azure.functions as func
from Security.key_agreement import KEY_AGREEMENT
from Constant import msg_config

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    expected_param_name = 'PublicKey'
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
    client_pub_key = req_body.get(expected_param_name)
    if client_pub_key:
        key_exchange_alg = KEY_AGREEMENT()
        kex_result, ret_msg = key_exchange_alg.key_exchange(client_pub_key)
        response = {
            'Code': msg_config.FUNC_CALL_SUCCESS_CODE
        }
        response.update(ret_msg)
        if kex_result:
            return func.HttpResponse(
                        json.dumps(response), 
                        mimetype = "application/json", 
                        status_code = 200
                    )
        else:
            response = {
                'Code': msg_config.KEX_GEN_FAILED_CODE,
                'Message': msg_config.KEX_GEN_FAILED
            }
            return func.HttpResponse(
                        json.dumps(response), 
                        mimetype = "application/json", 
                        status_code = 500
                    )
    else:
        response = {
            'Code': msg_config.HTTP_REQ_PARAMS_MISSING_CODE,
            'Message': msg_config.HTTP_REQ_PARAMS_MISSING.format(param_name = expected_param_name)
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 400
                )
