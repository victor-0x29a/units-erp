class InvalidParam(Exception):
    def __init__(self, message: str = "Have an invalid param."):
        self.message = message
        self.code = 1070
        super().__init__(self.message, self.code)
