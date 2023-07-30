import json, sys
from playfab import PlayFabAdminAPI, PlayFabSettings
sys.path.append('..')
from Constant import server_config

PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
PlayFabSettings.DeveloperSecretKey = server_config.X_SECRET_KEY

def callback(success: any, fail: any) -> None:
    if success:
        print(success['Statements'])
    if fail:
        print('fail')

def get_policy() -> None:
    request = {"PolicyName": "ApiPolicy"}
    PlayFabAdminAPI.GetPolicy(request, callback)

def update_policy() -> None:
    policy = json.load(open('./new_policy.json'))
    PlayFabAdminAPI.UpdatePolicy(policy, callback)

if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == 'get':
        get_policy()
    if arg == 'update':
        update_policy()