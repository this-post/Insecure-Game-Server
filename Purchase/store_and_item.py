import azure.functions as func
from Security import authorize_check
from PlayFabUtil.Admin.purchasing import PURCHASING
from PlayFabUtil.Admin.economy import ECONOMY
from PlayFabUtil.User.authorize import AUTHORIZE
from PlayFabUtil.Admin.profile import PROFILE
from HttpMessageHandling import request_validation, response_handler, request_model, request_handler, response_model
from urllib.parse import urlparse

class BUY_SELL_ITEM_DTO:
    def __init__(self, item_id: str = None) -> None:
        self.ItemId = item_id

class GET_BALANCE_DTO:
    def __init__(self, playfab_id: str = None) -> None:
        self.PlayFabId = playfab_id

from enum import Enum
class PURCHASING_URLS(str, Enum):
    SELL_URI = '/api/Purchase/Sell'
    BUY_URI = '/api/Purchase/Buy'
    BALANCE_URI = '/api/Purchase/Balance'
    CATALOG_URI = '/api/Purchase/Catalog'

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    is_x_auth_header = authorize_check.is_contain_x_auth_header(req)
    is_x_entity_token_header = authorize_check.is_contain_x_entity_token_header(req)
    if not is_x_auth_header or not is_x_entity_token_header:
        return response_handler.send_unauth_response()
    x_auth_header = authorize_check.get_x_auth(req)
    x_entity_token_header = authorize_check.get_x_entity_token(req)
    authorize = AUTHORIZE(
        session_ticket = x_auth_header,
        entity_token = x_entity_token_header
    )
    if not authorize.is_valid_session_ticket():
        return response_handler.send_unauth_response()
    try:
        playfab_id = authorize.get_playfab_id_from_entity_id()
    except ValueError:
        return response_handler.send_playfab_get_id_fail()
    match parse_url(req.url):
        case PURCHASING_URLS.SELL_URI:
            print(PURCHASING_URLS.SELL_URI.value)
            result = get_decrypted_request(req, context)
            # if isinstance(result, dict):
            if isinstance(result, request_model.COMMON_REQUEST_DTO):
                return sell(result, x_auth_header, playfab_id)
            else:
                return result
        case PURCHASING_URLS.BUY_URI:
            print(PURCHASING_URLS.BUY_URI.value)
            result = get_decrypted_request(req, context)
            if isinstance(result, request_model.COMMON_REQUEST_DTO):
                return buy(result, x_auth_header, playfab_id)
            else:
                return result
        case PURCHASING_URLS.BALANCE_URI:
            print(PURCHASING_URLS.BALANCE_URI.value)
            # result = get_decrypted_request(req, context)
            # if isinstance(result.__dict__, request_model.COMMON_REQUEST_DTO):
            #     return get_balance(result, x_entity_token_header)
            # else:
            #     return result
            if not request_validation.is_valid_json(req, context):
                return response_handler.send_invalid_json_response()
            req_body = req.get_json()
            request_dto = request_model.NO_DATA_REQUEST_DTO(
                key_id = req_body.get('KeyId')
            )
            is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
            if is_missing_param:
                return response_handler.send_missing_params_response(missing_key)
            return get_balance(request_dto.KeyId, playfab_id)
        case PURCHASING_URLS.CATALOG_URI:
            print(PURCHASING_URLS.CATALOG_URI.value)
            if not request_validation.is_valid_json(req, context):
                return response_handler.send_invalid_json_response()
            req_body = req.get_json()
            request_dto = request_model.NO_DATA_REQUEST_DTO(
                key_id = req_body.get('KeyId')
            )
            is_missing_param, missing_key = request_validation.is_missing_param(request_dto)
            if is_missing_param:
                return response_handler.send_missing_params_response(missing_key)
            return get_catalog_items(request_dto.KeyId)
        case _:
            return response_handler.send_not_found_response()

def parse_url(url: func.HttpRequest.url) -> str:
    parsed = urlparse(url)
    return parsed.path

def get_decrypted_request(req: func.HttpRequest, context: func.Context) -> any:
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
    return request_model.COMMON_REQUEST_DTO(
            key_id = request_dto.KeyId,
            data = request_handler.decrypt(request_dto)
        )

class BUY_SELL_RESPONSE_DTO:
    def __init__(self, success: bool = None, updated_balance: int = None) -> None:
        self.Success = success
        self.UpdatedBalance = updated_balance

def sell(decrypted_request_model: request_model.COMMON_REQUEST_DTO, x_auth_header: str, playfab_id: str) -> func.HttpResponse:
    playfab_sell_dto = BUY_SELL_ITEM_DTO(
        item_id = decrypted_request_model.Data.get('ItemId')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(playfab_sell_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    if not is_item_exist(playfab_sell_dto.ItemId, playfab_id):
        return response_handler.send_playfab_item_does_not_exist()
    playfab_purchasing = PURCHASING()
    try:
        item_price = playfab_purchasing.get_item_price_by_id(playfab_sell_dto.ItemId)
    except KeyError:
        return response_handler.send_playfab_item_does_not_exist()
    except ValueError:
        return response_handler.send_playfab_get_item_price_error()
    try:
        playfab_purchasing.revoke_user_item(playfab_id, playfab_sell_dto.ItemId)
    except ValueError:
        return response_handler.send_playfab_revoke_item_fail()
    try:
        playfab_purchasing.add_coin(playfab_id, item_price)
        buy_sell_response_dto = BUY_SELL_RESPONSE_DTO(
            success = True,
            updated_balance = playfab_purchasing.get_balance_by_user_id(playfab_id)
        )
        result_dto = response_model.PLAYFAB_COMMON_RESPONSE_DTO(
            success = buy_sell_response_dto.__dict__
        )
        return response_handler.send_common_response(decrypted_request_model.KeyId, result_dto)
    except ValueError:
        # grant an item since a coin addition is failed, we hope grant_item_to_user() won't throw an exception :(, or impelement new smart rollback method
        playfab_purchasing.grant_item_to_user(playfab_id, playfab_sell_dto.ItemId)
        return response_handler.send_playfab_revoke_item_fail()


def buy(decrypted_request_model: request_model.COMMON_REQUEST_DTO, x_auth_header: str, playfab_id: str) -> func.HttpResponse:
    playfab_buy_dto = BUY_SELL_ITEM_DTO(
        item_id = decrypted_request_model.Data.get('ItemId')
    )
    is_missing_param, missing_key = request_validation.is_missing_param(playfab_buy_dto)
    if is_missing_param:
        return response_handler.send_missing_params_response(missing_key)
    if is_item_exist(playfab_buy_dto.ItemId, playfab_id):
        return response_handler.send_playfab_item_exists()
    playfab_purchasing = PURCHASING()
    try:
        user_balance = playfab_purchasing.get_balance_by_user_id(playfab_id)
    except ValueError:
        return response_handler.send_playfab_get_balance_error()
    try:
        item_price = playfab_purchasing.get_item_price_by_id(playfab_buy_dto.ItemId)
    except KeyError:
        return response_handler.send_playfab_item_does_not_exist()
    except ValueError:
        return response_handler.send_playfab_get_item_price_error()
    if item_price > user_balance:
        return response_handler.send_playfab_insufficient_fund()
    try:
        playfab_purchasing.grant_item_to_user(playfab_id, playfab_buy_dto.ItemId)
    except ValueError:
        return response_handler.send_playfab_grant_item_fail()
    try:
        playfab_purchasing.subtract_coin(playfab_id, item_price)
        buy_sell_response_dto = BUY_SELL_RESPONSE_DTO(
            success = True,
            updated_balance = playfab_purchasing.get_balance_by_user_id(playfab_id)
        )
        result_dto = response_model.PLAYFAB_COMMON_RESPONSE_DTO(
            success = buy_sell_response_dto.__dict__
        )
        return response_handler.send_common_response(decrypted_request_model.KeyId, result_dto)
    except ValueError:
        # revoke an item since a coin subtraction is failed, we hope revoke_user_item() won't throw an exception :(, or impelement new smart rollback method
        playfab_purchasing.revoke_user_item(playfab_id, playfab_buy_dto.ItemId)
        return response_handler.send_playfab_grant_item_fail()

class GET_INVENTORY_DTO:
    def __init__(self, playfab_id: str = None) -> None:
        self.PlayFabId = playfab_id

def is_item_exist(item_id: str, playfab_id: str) -> bool:
    profile = PROFILE()
    playfab_get_user_inventory_dto = GET_INVENTORY_DTO(
        playfab_id = playfab_id
    )
    profile.get_user_inventory(playfab_get_user_inventory_dto)
    if profile.success:
        inventory = profile.success['Inventory']
        for items in inventory:
            if items['ItemId'] == item_id:
                return True
        return False
    else:
        return False

class BALANCE_RESPONSE_DTO:
    def __init__(self, balance: int = None) -> None:
        self.Balance = balance

# def get_balance(decrypted_json_object: dict, x_entity_token: str) -> func.HttpResponse:
def get_balance(key_id: str, playfab_id: str) -> func.HttpResponse:
    # playfab_get_balance_dto = GET_BALANCE_DTO(
    #     playfab_id = decrypted_json_object.get('PlayFabId')
    # )
    # is_missing_param, missing_key = request_validation.is_missing_param(playfab_get_balance_dto)
    # if is_missing_param:
    #     return response_handler.send_missing_params_response(missing_key)
    # authorize = AUTHORIZE(
    #     entity_token = x_entity_token
    # )
    # is_x_entity_token = authorize.is_authorize(playfab_get_balance_dto.PlayFabId)
    # if not is_x_entity_token:
    #     return response_handler.send_unauth_response()
    playfab_purchasing = PURCHASING()
    try:
        balance = playfab_purchasing.get_balance_by_user_id(playfab_id)
        balance_response_dto = BALANCE_RESPONSE_DTO(
            balance = balance
        )
        result_dto = response_model.PLAYFAB_COMMON_RESPONSE_DTO(
            success = balance_response_dto.__dict__
        )
        return response_handler.send_common_response(key_id, result_dto)
    except ValueError:
        return response_handler.send_playfab_get_balance_error()
    
def get_catalog_items(key_id: str) -> func.HttpResponse:
    playfab_catalog = ECONOMY()
    catalog = playfab_catalog.get_catalog_items()
    if catalog:
        result_dto = response_model.PLAYFAB_COMMON_RESPONSE_DTO(
            success = catalog
        )
        return response_handler.send_common_response(key_id, result_dto)
    else:
        return response_handler.send_playfab_get_catalog_error()