class LessThanCurrentDate(Exception):
    def __init__(self, message: str = "Expiry date must be greater than current date."):
        self.message = message
        self.code = 1003
        super().__init__(self.message, self.code)
