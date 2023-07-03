import azure.functions as func
from PlayFabUtil.register import REGISTER
from HttpMessageHandling import request_validation, response_handler

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    json_data, kid = request_validation.validate_encrypted_params(req, context)
    request_validation.validate_decrypted_params(json_data.items())
    email = json_data.get('Email')
    passwd = json_data.get('Password')
    is_require_username = json_data.get('RequireBothUsernameAndEmail')
    playfab_register_req = {
        'Email': email,
        'Password': passwd,
        'RequireBothUsernameAndEmail': is_require_username
    }
    playfab_register = REGISTER()
    playfab_register.register_with_email(playfab_register_req)
    return response_handler.send_response(kid, playfab_register)