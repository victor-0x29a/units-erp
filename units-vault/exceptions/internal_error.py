class InternalError(Exception):
    def __init__(self, message: str = "Internal error occurred."):
        self.message = message
        self.code = 500
        super().__init__(self.message, self.code)
