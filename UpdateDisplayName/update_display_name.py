import azure.functions as func
from PlayFabUtil.Admin.profile import PROFILE
from PlayFabUtil.User.authorize import AUTHORIZE
from Security import authorize_check
from HttpMessageHandling import request_validation, response_handler, request_model, request_handler

class UPDATE_DISPLAY_NAME_DTO:
    def __init__(self, display_name: str, playfab_id: str) -> None:
        self.PlayFabId = playfab_id
        self.DisplayName = display_name

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    if not request_validation.is_valid_json(req, context):
        return response_handler.send_invalid_json_response()
    req_body = req.get_json()
    is_x_auth_header = authorize_check.is_contain_x_auth_header(req)
    if not is_x_auth_header:
        return response_handler.send_unauth_response()
    x_auth_header = authorize_check.get_x_auth(req)
    authorize = AUTHORIZE(
        session_ticket = x_auth_header
    )
    if not authorize.is_valid_session_ticket():
        return response_handler.send_unauth_response()
    try:
        playfab_id = authorize.get_playfab_id_from_entity_id()
    except ValueError:
        return response_handler.send_playfab_get_id_fail()
    request_dto = request_model.COMMON_REQUEST_DTO(
        key_id = req_body.get('KeyId'),
        data = req_body.get('Data')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    decrypted_json_object = request_handler.decrypt(request_dto)
    # display_name = json_data.get('DisplayName')
    # playfab_update_user_title_display_name_req = {
    #     'DisplayName': display_name
    # }
    playfab_update_display_name_dto = UPDATE_DISPLAY_NAME_DTO(
        playfab_id = playfab_id,
        display_name = decrypted_json_object.get('DisplayName')
    )
    playfab_update_user_title_display_name = PROFILE()
    playfab_update_user_title_display_name.update_display_name(playfab_update_display_name_dto)
    return response_handler.send_common_response(request_dto.KeyId, playfab_update_user_title_display_name)