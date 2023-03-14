import requests

from stock import Stock


class StockMarket:

    def __init__(self):
        self.storks: dict[str, Stock] = {}

    def stock_price(self, stock: str) -> float:
        return self.stocks[stock].price

    def fetch_stock_market_data(self):
        res = requests.get("stockMarket.com/api/stocks")
        data = res.json()
        for stock in data:
            self.stocks[stock["name"]] = Stock(stock["name"], stock["price"])
