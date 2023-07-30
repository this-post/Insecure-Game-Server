from playfab import PlayFabAdminAPI, PlayFabSettings
from Constant import server_config

class ECONOMY:
    def __init__(self) -> None:
        PlayFabSettings.TitleId = server_config.PLAYFAB_TITLE_ID
        PlayFabSettings.DeveloperSecretKey = server_config.X_SECRET_KEY

    def callback(self, success, failure) -> None:
        self.success = success
        self.failure = failure

    def get_catalog_items(self) -> dict:
        request = {
            'CatalogVersion': server_config.CHARACTER_CATALOG_NAME
        }
        PlayFabAdminAPI.GetCatalogItems(request, self.callback)
        if self.failure:
            return {}
        if self.success:
            return self.success
        
    def get_catalog_item_by_id(self, item_id: str) -> dict:
        catalog = self.get_catalog_items()
        if catalog:
            for items in catalog['Catalog']:
                if items['ItemId'] == item_id:
                    return items
        return {} # should not be reached here since the existence of an item is checked first at buy()