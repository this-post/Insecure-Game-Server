# Insecure-Game-Server

## Generate the server's private key
```bash
cd PrivKey
./gen_priv_key.sh
```

## Choosing Azure Redis or local Redis
In `Constant/server_config.py`
```python
# Local Redis
IS_TESTING_ENV_REDIS = True

# Azure Redis (SSL port only)
IS_TESTING_ENV_REDIS = False
```
### If local Redis is chosen
```bash
docker pull redis
docker run --rm -p 6379:6379 -d redis
```

## Enter your PlayFab Developer Secret
In `Constant/server_config.py`
```python
# PlayFab Admin secret key
X_SECRET_KEY = ''
```