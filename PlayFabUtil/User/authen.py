import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class AUTHEN:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID

    def callback(self, success, failure) -> None:
            self.success = success
            self.failure = failure

    def login_with_email(self, request) -> None:
        request_dict = request.__dict__
        logging.info('Login with Email: {0}, Password: {1}'.format(request_dict['Email'], request_dict['Password']))
        PlayFabClientAPI.LoginWithEmailAddress(request_dict, self.callback)