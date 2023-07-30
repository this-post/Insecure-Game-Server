import azure.functions as func
import json, logging
from Constant import msg_config, server_config
from Security.aes_gcm import AES_GCM
from . import request_model, response_handler

def is_valid_json(req, context) -> bool:
    try:
        req_body = req.get_json()
        logging.info(msg_config.FUNC_CALL_LOG.format(function_name = context.function_name, json_body = str(req_body)))
        return True
    except ValueError:
        return False

def is_missing_param(object_dto: any) -> tuple[bool, str]:
    dict_of_params = object_dto.__dict__.items()
    for k, v in dict_of_params:
        if not v or not k:
            return True, k # return each missing param
    return False, ''