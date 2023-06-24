# Redis
REDIS_HOST = 'vulb.redis.cache.windows.net'
REDIS_PWD = 'uh2ORVR4wUqhq0U3OECgHe2ykWNnszfAZAzCaEZ3kJA='
REDIS_SSL_PORT = 6380
REDIS_NON_SSL_PORT = 6379
IS_TESTING_ENV_REDIS = True

# PlayFab URL, wildcard Cert, the sub-domain can be ANY
PLAYFAB_TITLE_ID = 'cc95c'
PLAYFAB_URL = '{0}.playfabapi.com'.format(PLAYFAB_TITLE_ID)

# Azure URL, wildcard Cert, the sub-domain can be ANY
AZURE_SUB_DOMAIN = 'msdcinfo' # Microsoft owned sub-domain
AZURE_URL = '{0}.azurewebsites.net'.format(AZURE_SUB_DOMAIN)

# Certificate Pinning
from enum import Enum
class Trusted_URLs(str, Enum):
    playfab = PLAYFAB_URL
    azure = AZURE_URL

# Key agreement
PRIV_KEY_PATH = './PrivKey/ec521-priv.pem'
