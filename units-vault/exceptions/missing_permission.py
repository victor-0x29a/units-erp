class MissingPermission(Exception):
    def __init__(self, message: str = "Has missing permission."):
        self.message = message
        self.code = 1556
        super().__init__(self.message, self.code)
