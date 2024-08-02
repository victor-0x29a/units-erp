class GreaterThanPrice(Exception):
    def __init__(self, message: str = "The discount is greater than the price of the product."):
        self.message = message
        self.code = 1009
        super().__init__(self.message, self.code)
