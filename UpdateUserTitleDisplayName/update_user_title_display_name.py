import azure.functions as func
from PlayFabUtil.profile import PROFILE
from Security import authorize_check
from HttpMessageHandling import request_validation, response_handler

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    x_auth_header = authorize_check.is_contain_x_auth_header(req)
    json_data, kid = request_validation.validate_encrypted_params(req, context)
    request_validation.validate_decrypted_params(json_data.items())
    display_name = json_data.get('DisplayName')
    playfab_update_user_title_display_name_req = {
        'DisplayName': display_name
    }
    playfab_update_user_title_display_name = PROFILE(x_auth_header)
    playfab_update_user_title_display_name.update_display_name(playfab_update_user_title_display_name_req)
    return response_handler.send_response(kid, playfab_update_user_title_display_name)