class MissingDoc(Exception):
    def __init__(self, message: str = "Has missing doc."):
        self.message = message
        self.code = 1003
        super().__init__(self.message, self.code)
