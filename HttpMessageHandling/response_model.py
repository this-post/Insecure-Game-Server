class COMMON_RESPONSE_DTO():
    def __init__(self, code = None, message = None) -> None:
        self.Code = code
        self.Message = message

class PLAYFAB_COMMON_RESPONSE_DTO():
    def __init__(self, success: any = None, fail: any = None) -> None:
        self.success = success
        self.fail = fail