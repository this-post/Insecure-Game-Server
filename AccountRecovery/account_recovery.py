import azure.functions as func
from PlayFabUtil.recovery import RECOVERY
from HttpMessageHandling import request_validation, response_handler
from Constant import server_config

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    json_data, kid = request_validation.validate_encrypted_params(req, context)
    request_validation.validate_decrypted_params(json_data.items())
    email = json_data.get('Email')
    playfab_recovery_request ={
        'Email': email,
        'TitleId': server_config.PLAYFAB_TITLE_ID # this must be explicitly specified, otherwise, errorCode: 1131 will be raised
    }
    playfab_recovery = RECOVERY()
    playfab_recovery.recovery_with_email(playfab_recovery_request)
    return response_handler.send_response(kid, playfab_recovery)