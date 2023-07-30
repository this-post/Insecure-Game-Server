import azure.functions as func
from PlayFabUtil.User.authen import AUTHEN
from HttpMessageHandling import request_validation, response_handler, request_model, request_handler

class LOGIN_DTO:
    def __init__(self, email: str = None, password: str = None) -> None:
        self.Email = email
        self.Password = password

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
    playfab_auth_dto = LOGIN_DTO(
        email = decrypted_json_object.get('Email'),
        password = decrypted_json_object.get('Password')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(playfab_auth_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    playfab_auth = AUTHEN()
    playfab_auth.login_with_email(playfab_auth_dto)
    return response_handler.send_common_response(request_dto.KeyId, playfab_auth)
