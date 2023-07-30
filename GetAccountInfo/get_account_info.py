import azure.functions as func
from PlayFabUtil.Admin.profile import PROFILE
from PlayFabUtil.User.authorize import AUTHORIZE
from Security import authorize_check
from HttpMessageHandling import request_validation, response_handler, request_model
import logging

class GET_ACCOUNT_INFO_DTO:
    def __init__(self, playfab_id: str = None, ignore_missing_title_activation: bool = None) -> None:
        self.PlayFabId = playfab_id
        self.IgnoreMissingTitleActivation = ignore_missing_title_activation

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
    playfab_id = authorize.get_playfab_id_from_entity_id()
    # request_dto = request_model.COMMON_REQUEST_DTO(
    #     key_id = req_body.get('KeyId'),
    #     data = req_body.get('Data')
    # )
    request_dto = request_model.NO_DATA_REQUEST_DTO(
        key_id = req_body.get('KeyId')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    # decrypted_json_object = request_handler.decrypt(request_dto)
    # playfab_get_acc_info_dto = GET_ACCOUNT_INFO_DTO(
    #     playfab_id = decrypted_json_object.get('PlayFabId')
    # )
    # is_missing_param, missing_key = request_validation.is_missing_param(playfab_get_acc_info_dto)
    # if is_missing_param:
    #     return response_handler.send_missing_params_response(missing_key)
    # playfab_get_acc_info = PROFILE(x_auth_header)
    # playfab_get_acc_info.get_account_info(playfab_get_acc_info_dto)
    playfab_get_acc_info_dto = GET_ACCOUNT_INFO_DTO(
        playfab_id = playfab_id,
        ignore_missing_title_activation = False
    )
    playfab_get_acc_info = PROFILE()
    playfab_get_acc_info.get_account_info(playfab_get_acc_info_dto)
    return response_handler.send_common_response(request_dto.KeyId, playfab_get_acc_info)