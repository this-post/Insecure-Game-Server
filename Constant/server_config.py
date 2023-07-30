# Redis
REDIS_HOST = 'vulb.redis.cache.windows.net'
REDIS_PWD = 'uh2ORVR4wUqhq0U3OECgHe2ykWNnszfAZAzCaEZ3kJA='
REDIS_SSL_PORT = 6380
REDIS_NON_SSL_PORT = 6379
IS_TESTING_ENV_REDIS = True

# PlayFab Admin secret key
X_SECRET_KEY = ''

# PlayFab in-game constant
STORE_ID = 'Vul Busters Store'
VIRTUAL_CURRENCY_CODE = 'VB'
CHARACTER_CATALOG_NAME = 'Character'

# PlayFab URL, wildcard Cert, the sub-domain can be ANY
PLAYFAB_TITLE_ID = 'cc95c'
PLAYFAB_URL = '{0}.playfabapi.com'.format(PLAYFAB_TITLE_ID)

# Azure URL, wildcard Cert, the sub-domain can be ANY
# AZURE_SUB_DOMAIN = 'msdcinfo' # Microsoft owned sub-domain, GONE
AZURE_SUB_DOMAIN = 'azuredatacentermap'
# AZURE_SUB_DOMAIN = 'vulb'
AZURE_URL = '{0}.azurewebsites.net'.format(AZURE_SUB_DOMAIN)
BLOB_URL = 'vulbusters.blob.core.windows.net'

# Certificate Pinning
from enum import Enum
class TRUSTED_URLS(str, Enum):
    playfab = PLAYFAB_URL
    azure = AZURE_URL
    blob = BLOB_URL

# Key agreement
PRIV_KEY_PATH = './PrivKey/ec521-priv.pem'

# HTTP request headers
X_AUTH_HEADER = 'X-Authorization'
X_ENTITY_TOKEN_HEADER = 'X-EntityToken'

# HTTP response headers
CONTENT_JSON = 'application/json'

# HTTP response code
OK_CODE = 200
BAD_REQ_CODE = 400
UNAUTH_CODE = 403
NOT_FOUND_CODE = 404
INTERNAL_ERROR_CODE = 500