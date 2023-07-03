import azure.functions as func
from PlayFabUtil.profile import PROFILE
from Security import authorize_check
from HttpMessageHandling import request_validation, response_handler

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    x_auth_header = authorize_check.is_contain_x_auth_header(req)
    json_data, kid = request_validation.validate_encrypted_params(req, context)
    request_validation.validate_decrypted_params(json_data.items())
    playfab_id = json_data.get('PlayFabId')
    playfab_get_acc_info_req = {
        'PlayFabId': playfab_id
    }
    playfab_get_acc_info = PROFILE(x_auth_header)
    playfab_get_acc_info.get_account_info(playfab_get_acc_info_req)
    return response_handler.send_response(kid, playfab_get_acc_info)