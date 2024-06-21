class HasWithSameBatch(Exception):
    def __init__(self, message: str = "Already has product with the same batch."):
        self.message = message
        self.code = 1002
        super().__init__(self.message, self.code)
