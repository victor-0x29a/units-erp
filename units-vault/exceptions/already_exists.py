class AlreadyExists(Exception):
    def __init__(self, message: str = "Already exists."):
        self.message = message
        self.code = 1003
        super().__init__(self.message, self.code)
