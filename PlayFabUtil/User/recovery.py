import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class RECOVERY:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID

    def callback(self, success, failure) -> None:
            if failure:
                self.failure = failure
                self.success = {}
            else:
                self.failure = {}
                self.success = {'EmailSent': True} # The successful operation will always return an empty object that let's the response_handler.send_common_response() is error, so, we just set our own result to prevent null object
    
    def recovery_with_email(self, request) -> None:
        request_dict = request.__dict__
        logging.info('Recovery with Email: {0}'.format(request_dict['Email']))
        PlayFabClientAPI.SendAccountRecoveryEmail(request_dict, self.callback)