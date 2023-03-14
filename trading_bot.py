from stock_market import StockMarket
from trade_transaction import TradeTransaction, TransactionType


class TradingBot:
    """
    A trading bot that buys and sells stocks based on a given strategy.
    """

    def __init__(self, cash: float, stock_market: StockMarket):
        self.cash = cash
        self.portfolio: dict[str, int] = {}
        self.stock_market = stock_market
        self.historical_transactions: list[TradeTransaction] = []

    def sell_stock(self, stock: str, amount: int):
        """
        Sells a given amount of a stock. If the stock is not in the portfolio,
        raises a ValueError. If the amount is greater than the amount owned,
        raises a ValueError.
        """

        if stock not in self.portfolio:
            raise ValueError(f"You don't own any {stock}")
        if self.portfolio[stock] < amount:
            raise ValueError(f"You don't own enough {stock}")

        self.portfolio[stock] -= amount
        self.cash += amount * self.stock_market.stock_price(stock)

        transaction = TradeTransaction(
            len(self.historical_transactions), TransactionType.SELL, self.stock_market.stock_price(stock), amount, stock)
        self.historical_transactions.append(transaction)

    def buy_stock(self, stock: str, amount: int):
        """
        Buys a given amount of a stock. If the amount is greater than the
        amount of cash owned, raises a ValueError.
        """

        if self.cash < amount * self.stock_market.stock_price(stock):
            raise ValueError(
                f"You don't have enough cash to buy {amount} of {stock}")

        self.cash -= amount * self.stock_market.stock_price(stock)
        self.portfolio[stock] += amount

        transaction = TradeTransaction(
            len(self.historical_transactions), TransactionType.BUY, self.stock_market.stock_price(stock), amount, stock)
        self.historical_transactions.append(transaction)

    def get_portfolio_value(self) -> float:
        """
        Returns the total value of the portfolio, including cash.
        """

        value = self.cash
        for stock, amount in self.portfolio.items():
            value += amount * self.stock_market.stock_price(stock)
        return value
