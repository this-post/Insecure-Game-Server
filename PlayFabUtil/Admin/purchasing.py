from playfab import PlayFabAdminAPI, PlayFabSettings
from . import economy
from Constant import server_config

class GET_ITEM_PRICE_DTO:
    def __init__(self, store_id: str = None) -> None:
        self.StoreId = store_id

class SUBTRACT_COIN_DTO:
    def __init__(self, playfab_id: str = None, virtual_currency: str = None, amount: int = None) -> None:
        self.PlayFabId = playfab_id
        self.VirtualCurrency = virtual_currency
        self.Amount = amount

class ADD_COIN_DTO:
    def __init__(self, playfab_id: str = None, virtual_currency: str = None, amount: int = None) -> None:
        self.PlayFabId = playfab_id
        self.VirtualCurrency = virtual_currency
        self.Amount = amount

class GET_USER_BALANCE_DTO:
    def __init__(self, playfab_id: str = None) -> None:
        self.PlayFabId = playfab_id

class GET_ITEM_INSTANCE_ID_DTO:
    def __init__(self, playfab_id: str = None) -> None:
        self.PlayFabId = playfab_id

class REVOKE_ITEM_DTO:
    def __init__(self, playfab_id: str = None, item_instance_id: str = None) -> None:
        self.PlayFabId = playfab_id
        self.ItemInstanceId = item_instance_id

class GRANT_ITEM_DTO:
    def __init__(self, catalog_version: str = None, item_grants: list = None) -> None:
        self.CatalogVetsion = catalog_version
        self.ItemGrants = item_grants

class ITEM_BEING_GRANTED_DTO:
    def __init__(self, playfab_id: str = None, item_id: str = None, data: dict = None) -> None:
        self.PlayFabId = playfab_id
        self.ItemId = item_id
        self.Data = data

class PURCHASING():
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
        PlayFabSettings.DeveloperSecretKey = server_config.X_SECRET_KEY

    def callback(self, success: any, fail: any) -> None:
        self.success = success
        self.fail = fail

    # GetItem API on EconomyV2 allow only paid PlayFab account, so, we use this instead
    def get_item_price_by_id(self, item_id: str) -> int:
        request_dto = GET_ITEM_PRICE_DTO(
            store_id = server_config.STORE_ID
        )
        PlayFabAdminAPI.GetStoreItems(request_dto.__dict__, self.callback)
        if self.success:
            store = self.success['Store']
            for items in store:
                if items['ItemId'] == item_id:
                    return items['VirtualCurrencyPrices'][server_config.VIRTUAL_CURRENCY_CODE]
            raise KeyError('No item found')
        if self.fail:
            raise ValueError('Unable to get price')
        
    def subtract_coin(self, playfab_id: str, amount: int) -> int:
        request_dto = SUBTRACT_COIN_DTO(
            playfab_id = playfab_id,
            virtual_currency = server_config.VIRTUAL_CURRENCY_CODE,
            amount = amount
        )
        PlayFabAdminAPI.SubtractUserVirtualCurrency(request_dto.__dict__, self.callback)
        if self.success:
            return self.success['Balance'] # balance
        if self.fail:
            raise ValueError('Unable to subtract the coins')
        
    def add_coin(self, playfab_id: str, amount: int) -> int:
        request_dto = ADD_COIN_DTO(
            playfab_id = playfab_id,
            virtual_currency = server_config.VIRTUAL_CURRENCY_CODE,
            amount = amount
        )
        PlayFabAdminAPI.AddUserVirtualCurrency(request_dto.__dict__, self.callback)
        if self.success:
            return self.success['Balance'] # balance
        if self.fail:
            raise ValueError('Unable to subtract the coins')
        
    def get_balance_by_user_id(self, playfab_id: str) -> int:
        request_dto = GET_USER_BALANCE_DTO(
            playfab_id = playfab_id
        )
        PlayFabAdminAPI.GetUserInventory(request_dto.__dict__, self.callback)
        if self.success:
            return self.success['VirtualCurrency'][server_config.VIRTUAL_CURRENCY_CODE]
        if self.fail:
            raise ValueError('Unable to get balance')
        
    def grant_item_to_user(self, playfab_id: str, item_id: str) -> None:
        # request = {
        #     'CatalogVersion': server_config.CHARACTER_CATALOG_NAME,
        #     'ItemGrants': [
        #         {
        #             'PlayFabId': playfab_id,
        #             'ItemId': item_id
        #         }
        #     ],
        #     'Data': {
        #         'Signature': signature
        #     }
        # }
        _economy = economy.ECONOMY()
        item_info = _economy.get_catalog_item_by_id(item_id)
        item_image_url = item_info['ItemImageUrl']
        granted_item = ITEM_BEING_GRANTED_DTO(
            playfab_id = playfab_id,
            item_id = item_id,
            data = {
                'ItemImageUrl': item_image_url
            }
        )
        request_dto = GRANT_ITEM_DTO(
            catalog_version = server_config.CHARACTER_CATALOG_NAME,
            item_grants = [
                granted_item.__dict__
            ]
        )
        PlayFabAdminAPI.GrantItemsToUsers(request_dto.__dict__, self.callback)
        if self.fail:
            raise ValueError('Unable to grant an item')
        
    def get_item_instance_id_by_item_id(self, playfab_id: str, item_id: str) -> str:
        request_dto = GET_ITEM_INSTANCE_ID_DTO(
            playfab_id = playfab_id
        )
        PlayFabAdminAPI.GetUserInventory(request_dto.__dict__, self.callback)
        if self.success:
            inventory = self.success['Inventory']
            for items in inventory:
                if items['ItemId'] == item_id:
                    return items['ItemInstanceId']
            return ''
        if self.fail:
            raise ValueError('Unable to get balance')

    def revoke_user_item(self, playfab_id: str, item_id: str) -> None:
        item_instance_id = self.get_item_instance_id_by_item_id(playfab_id, item_id)
        if not item_instance_id:
            raise ValueError('Unable to get item instance ID')
        request_dto = REVOKE_ITEM_DTO(
            playfab_id = playfab_id,
            item_instance_id = item_instance_id
        )
        PlayFabAdminAPI.RevokeInventoryItem(request_dto.__dict__, self.callback)
        if self.fail:
            raise ValueError('Unable to revoke sn item')