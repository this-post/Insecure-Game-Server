class COMMON_REQUEST_DTO():
    def __init__(self, key_id: str = None, data: str = None) -> None:
        self.KeyId = key_id
        self.Data = data

class NO_DATA_REQUEST_DTO():
    def __init__(self, key_id: str = None) -> None:
        self.KeyId = key_id