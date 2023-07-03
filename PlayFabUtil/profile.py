import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class PROFILE:
    def __init__(self, sessionTicket) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
        if not sessionTicket:
            raise Exception('the session must be sent before call this')
        PlayFabSettings._internalSettings.ClientSessionTicket = sessionTicket

    def callback(self, success, failure) -> None:
        self.success = success
        self.failure = failure

    def get_account_info(self, request) -> None:
        logging.info('PlayFab ID: {0}'.format(request['PlayFabId']))
        PlayFabClientAPI.GetAccountInfo(request, self.callback)

    def update_display_name(self, request) -> None:
        logging.info('Display name: {0}'.format(request['DisplayName']))
        PlayFabClientAPI.UpdateUserTitleDisplayName(request, self.callback)