from Constant import server_config
import azure.functions as func

def is_contain_x_auth_header(req: func.HttpRequest) -> bool: # just validate the existence of it, PlayFab server will check the validity instead
    x_auth_header = req.headers.get(server_config.X_AUTH_HEADER)
    if not x_auth_header:
        return False
    return True

def get_x_auth(req: func.HttpRequest) -> str:
    return req.headers.get(server_config.X_AUTH_HEADER)

def is_contain_x_entity_token_header(req: func.HttpRequest) -> bool:
    x_entity_token_header = req.headers.get(server_config.X_ENTITY_TOKEN_HEADER)
    if not x_entity_token_header:
        return False
    return True

def get_x_entity_token(req: func.HttpRequest) -> str:
    return req.headers.get(server_config.X_ENTITY_TOKEN_HEADER)