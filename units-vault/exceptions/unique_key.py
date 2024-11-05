class UniqueKey(Exception):
    def __init__(self, message: str = "Failure at unique key validation."):
        self.message = message
        self.code = 1010
        super().__init__(self.message, self.code)
