import azure.functions as func
from PlayFabUtil.User.recovery import RECOVERY
from HttpMessageHandling import request_validation, response_handler, request_model, request_handler
from Constant import server_config

# use PlayFab service to validate email/title_id
class ACCOUNT_RECOVERY_DTO:
    def __init__(self, email: str = None, title_id: str = None) -> None:
        self.Email = email
        self.TitleId = title_id

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    if not request_validation.is_valid_json(req, context):
        return response_handler.send_invalid_json_response()
    req_body = req.get_json()
    request_dto = request_model.COMMON_REQUEST_DTO(
        key_id = req_body.get('KeyId'),
        data = req_body.get('Data')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    decrypted_json_object = request_handler.decrypt(request_dto)
    if not decrypted_json_object:
        response_handler.send_invalid_key_id_response()
    playfab_recovery_request = ACCOUNT_RECOVERY_DTO(
        email = decrypted_json_object.get('Email'),
        title_id = server_config.PLAYFAB_TITLE_ID # this must be explicitly specified, otherwise, errorCode: 1131 will be raised
    )
    is_missing_param, missing_key = request_validation.is_missing_param(playfab_recovery_request)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    playfab_recovery = RECOVERY()
    playfab_recovery.recovery_with_email(playfab_recovery_request)
    return response_handler.send_common_response(request_dto.KeyId, playfab_recovery)