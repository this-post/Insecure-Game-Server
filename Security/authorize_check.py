from Constant import msg_config, server_config
import azure.functions as func
import json

def is_contain_x_auth_header(req) -> str: # just validate the existence of it, PlayFab server will check the validity instead
    x_auth_header = req.headers.get(server_config.X_AUTH_HEADER)
    if not x_auth_header:
        response = {
            'Code': msg_config.HTTP_REQ_UNAUTH_CODE,
            'Message': msg_config.HTTP_REQ_UNAUTH
        }
        return func.HttpResponse(
                    json.dumps(response), 
                    mimetype = "application/json", 
                    status_code = 403
                )
    return x_auth_header