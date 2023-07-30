import logging
from playfab import PlayFabAdminAPI, PlayFabSettings
from Constant import server_config

class PROFILE:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
        PlayFabSettings.DeveloperSecretKey = server_config.X_SECRET_KEY

    def callback(self, success, failure) -> None:
        self.success = success
        self.failure = failure

    def get_account_info(self, request) -> None:
        request_dict = request.__dict__
        logging.info('PlayFab ID: {0}'.format(request_dict['PlayFabId']))
        PlayFabAdminAPI.GetUserAccountInfo(request_dict, self.callback)

    def get_user_inventory(self, request) -> None:
        request_dict = request.__dict__
        logging.info('PlayFab ID: {0}'.format(request_dict['PlayFabId']))
        PlayFabAdminAPI.GetUserInventory(request_dict, self.callback)

    def update_display_name(self, request) -> None:
        request_dict = request.__dict__
        logging.info('Display name: {0}'.format(request_dict['DisplayName']))
        PlayFabAdminAPI.UpdateUserTitleDisplayName(request_dict, self.callback)