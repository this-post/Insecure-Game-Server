import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class RECOVERY:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID

    def callback(self, success, failure) -> None:
            self.success = {'EmailSent': True} # The successful operation will always return an empty object that let's the response_handler.send_response() is error, so, we just set our own result to prevent null object
            self.failure = failure
    
    def recovery_with_email(self, request) -> None:
        logging.info('Recovery with Email: {0}'.format(request['Email']))
        PlayFabClientAPI.SendAccountRecoveryEmail(request, self.callback)