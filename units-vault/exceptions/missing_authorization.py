class MissingAuthorization(Exception):
    def __init__(self, message: str = "Has missing authorization."):
        self.message = message
        self.code = 1555
        super().__init__(self.message, self.code)
