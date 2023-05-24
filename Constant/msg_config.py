FUNC_CALL_SUCCESS_CODE = 0000

REDIS_KEY_NOT_FOUND_CODE = 1000
REDIS_KEY_NOT_FOUND_MSG = 'Key not found'

HTTP_REQ_IS_NOT_JSON_CODE = 2000
HTTP_REQ_IS_NOT_JSON = "HTTP request message is not JSON"
HTTP_REQ_PARAMS_MISSING_CODE = 2001
HTTP_REQ_PARAMS_MISSING = "`{param_name}` is missing"

KEX_INVALID_PUBKEY_CODE = 3000
KEX_INVALID_PUBKEY = "Invalid public key"
KEX_INVALID_DER_CODE = 3001
KEX_INVALID_DER = "Invalid DER structure"
KEX_GEN_KID_FAILED_CODE = 3002
KEX_GEN_KID_FAILED = "KID generation is failed"
KEX_GEN_INVALID_KID_CODE = 3003
KEX_GEN_INVALID_KID = "Invalid KID"
KEX_GEN_FAILED_CODE = 3004
KEX_GEN_FAILED = "Key agreement failed"

CERT_GET_URL_ERROR_CODE = 4000
CERT_GET_URL_ERROR = "Retrieving trusted URLs is failed"

UNKNOWN_ERROR_CODE = 9999
UNKNOWN_ERROR = "Unknown error"

# Logging message
FUNC_CALL_LOG = "Function: {function_name} \nRequest body: {json_body}"