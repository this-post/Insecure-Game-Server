import azure.functions as func
from PlayFabUtil.User.authorize import AUTHORIZE
from PlayFabUtil.Admin.profile import PROFILE
from Security import authorize_check
from HttpMessageHandling import request_validation, response_handler, request_model, request_handler

class GET_INVENTORY_DTO:
    def __init__(self, playfab_id: str = None) -> None:
        self.PlayFabId = playfab_id

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
    request_dto = request_model.NO_DATA_REQUEST_DTO(
        key_id = req_body.get('KeyId')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    try:
        playfab_id = authorize.get_playfab_id_from_entity_id()
    except ValueError:
        return response_handler.send_playfab_get_id_fail()
    playfab_get_user_inventory_dto = GET_INVENTORY_DTO(
        playfab_id = playfab_id
    )
    playfab_get_user_inventory = PROFILE()
    playfab_get_user_inventory.get_user_inventory(playfab_get_user_inventory_dto)
    return response_handler.send_common_response(request_dto.KeyId, playfab_get_user_inventory)