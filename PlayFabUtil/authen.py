import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class AUTHEN:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID

    def callback(self, success, failure):
            self.success = success
            # logging.info(success)
            self.failure = failure
            # logging.info(failure)

    def login_with_email(self, request):
        logging.info('Login with Email: {0}, Password: {1}'.format(request['Email'], request['Password']))
        request['TitleId'] = PlayFabSettings.TitleId
        PlayFabClientAPI.LoginWithEmailAddress(request, self.callback)