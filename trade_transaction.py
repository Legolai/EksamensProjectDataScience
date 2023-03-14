from enum import Enum
import time


class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"


class TradeTransaction:
    """
    A Trade Transaction class that represents a trade transaction.
    Contains the following attributes:
    - id: the id of the trade
    - type: the type of the trade
    - price: the price of the trade
    - amount: the amount of the trade
    - stock: the stock of the trade
    - time: the time of the trade
    """

    def __init__(self, id: int, type: TransactionType, price: float, amount: int, stock: str):
        self.id = id
        self.type = type
        self.price = price
        self.amount = amount
        self.stock = stock
        self.time = time.time()

    def __str__(self):
        return f"{self.id}: {self.type} {self.amount} of {self.stock} at {self.price} on {self.time}"
