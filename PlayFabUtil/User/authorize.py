# use only when Admin API is used on the client requests (e.g., Purchasing), otherwise, let's PlayFab check by itself
from Constant import server_config
from playfab import PlayFabAuthenticationAPI, PlayFabProfilesAPI, PlayFabSettings

class GET_PROFILE_DTO:
    def __init__(self, id: str = None, type: str = None, type_string: str = None) -> None:
        self.Id = id
        self.Type = type
        self.TypeString = type_string

class AUTHORIZE:
    def __init__(self, session_ticket: str = None, entity_token: str = None) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
        if not session_ticket:
            raise KeyError('the session must be sent before call this')
        PlayFabSettings._internalSettings.ClientSessionTicket = session_ticket
        PlayFabSettings._internalSettings.EntityToken = entity_token

    def callback(self, success: any, fail: any) -> None:
        if success:
            self.success = success
        if fail:
            self.fail = fail

    # use X-Authorization
    def is_valid_session_ticket(self) -> bool:
        request = {}
        PlayFabAuthenticationAPI.GetEntityToken(request, self.callback)
        if self.success['EntityToken']:
            self.entity_id = self.success['Entity']['Id']
            return True
        return False
    
    # use X-EntityToken
    # to prohibit an arbitrary PlayFab ID
    # call is_valid_session_ticket(self) first
    def is_authorize(self, playfab_id: str) -> bool:
        if not self.entity_id:
            return False
        playfab_get_profile_dto = GET_PROFILE_DTO(
            id = self.entity_id,
            type = 'title_player_account',
            type_string = 'title_player_account'
        )
        PlayFabProfilesAPI.GetProfile(playfab_get_profile_dto.__dict__, self.callback)
        if self.success['Profile']['Lineage']['MasterPlayerAccountId'] == playfab_id:
            return True
        return False
    
    # call is_valid_session_ticket(self) first
    # entity_id cannot be IDORed
    def get_playfab_id_from_entity_id(self) -> str:
        if not self.entity_id:
            return ''
        playfab_get_profile_dto = GET_PROFILE_DTO(
            id = self.entity_id,
            type = 'title_player_account',
            type_string = 'title_player_account'
        )
        PlayFabProfilesAPI.GetProfile(playfab_get_profile_dto.__dict__, self.callback)
        if self.success:
            return self.success['Profile']['Lineage']['MasterPlayerAccountId']
        if self.fail:
            raise ValueError('Unable to get PlayFab ID')