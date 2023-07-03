import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class REGISTER:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID

    def callback(self, success, failure) -> None:
        self.success = success
        self.failure = failure
    
    def register_with_email(self, request) -> None:
        logging.info('Register with Email: {0}, Password: {1}'.format(request['Email'], request['Password']))
        PlayFabClientAPI.RegisterPlayFabUser(request, self.callback)