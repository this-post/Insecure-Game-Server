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
