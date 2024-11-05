class MissingParam(Exception):
    def __init__(self, message: str = "Missing param."):
        self.message = message
        self.code = 1011
        super().__init__(self.message, self.code)
