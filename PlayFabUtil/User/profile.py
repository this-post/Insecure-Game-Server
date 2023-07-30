import logging
from playfab import PlayFabClientAPI, PlayFabSettings
from Constant import server_config

class PROFILE:
    def __init__(self, session_ticket: str) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
        if not session_ticket:
            raise KeyError('the session must be sent before call this')
        PlayFabSettings._internalSettings.ClientSessionTicket = session_ticket

    def callback(self, success, failure) -> None:
        self.success = success
        self.failure = failure

    # use Admin API
    # def get_user_inventory(self) -> None:
    #     PlayFabClientAPI.GetUserInventory(self.callback)

    # use Admin API
    # def get_account_info(self, request) -> None:
    #     request_dict = request.__dict__
    #     logging.info('PlayFab ID: {0}'.format(request_dict['PlayFabId']))
    #     PlayFabClientAPI.GetAccountInfo(request_dict, self.callback)

    # use Admin API
    # def update_display_name(self, request) -> None:
    #     request_dict = request.__dict__
    #     logging.info('Display name: {0}'.format(request_dict['DisplayName']))
    #     PlayFabClientAPI.UpdateUserTitleDisplayName(request_dict, self.callback)