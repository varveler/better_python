
# Template method design pattern is to define an algorithm as a skeleton of
# operations and leave the details to be implemented by the child classes.
# The overall structure and sequence of the algorithm is preserved
# by the parent class.

# Template means Preset format like HTML templates which has a fixed preset
# format. Similarly in the template method pattern, we have a preset
# structure method called template method which consists of steps.
# This steps can be an abstract method which will be implemented by its subclasses.

# This behavioral design pattern is one of the easiest
# to understand and implement. This design pattern is used popularly in
#framework development. This helps to avoid code duplication also.
#source: https://www.geeksforgeeks.org/template-method-design-pattern/


## All code and ideas from video https://youtu.be/eiDyK_ofPPM
## https://github.com/ArjanCodes/betterpython/tree/main/6%20-%20template%20method%20%26%20bridge
################################################################################
## BEFORE CODE ##
################################################################################


from typing import List

class Application:

    def __init__(self, trading_strategy = "average"):
        self.trading_strategy = trading_strategy

    def connect(self):
        print(f"Connecting to Crypto exchange...")

    def get_market_data(self, coin: str) -> List[float]:
        return [10, 12, 18, 14]

    def list_average(self, l: List[float]) -> float:
        return sum(l) / len(l)

    def should_buy(self, prices: List[float]) -> bool:
        if self.trading_strategy == "minmax":
            return prices[-1] == min(prices)
        else:
            return prices[-1] < self.list_average(prices)

    def should_sell(self, prices: List[float]) -> bool:
        if self.trading_strategy == "minmax":
            return prices[-1] == max(prices)
        else:
            return prices[-1] > self.list_average(prices)

    def check_prices(self, coin: str):
        self.connect()
        prices = self.get_market_data(coin)
        should_buy = self.should_buy(prices)
        should_sell = self.should_sell(prices)
        if should_buy:
            print(f"You should buy {coin}!")
        elif should_sell:
            print(f"You should sell {coin}!")
        else:
            print(f"No action needed for {coin}.")

application = Application("average")
application.check_prices("BTC/USD")


################################################################################
# CODE AFTER applying the template method
################################################################################
## what is nice about this code is that we can add an extra trading strategy
## whithout modify the original check prices method, so the process is standarized.
## but changes are possible without add to many boilerplate code.
## TradingBot class is our template class

from typing import List
from abc import ABC, abstractmethod

class TradingBot(ABC):
    def connect(self):
        print(f"Connecting to Crypto exchange...")

    def get_market_data(self, coin: str) -> List[float]:
        return [10, 12, 18, 14]

    @abstractmethod
    def should_buy(self, prices: List[float]) -> bool:
        pass

    @abstractmethod
    def should_sell(self, prices: List[float]) -> bool:
        pass

    def check_prices(self, coin: str):
        self.connect()
        prices = self.get_market_data(coin)
        should_buy = self.should_buy(prices)
        should_sell = self.should_sell(prices)
        if should_buy:
            print(f"You should buy {coin}!")
        elif should_sell:
            print(f"You should sell {coin}!")
        else:
            print(f"No action needed for {coin}.")

class AverageTrader(TradingBot):
    def list_average(self, l: List[float]) -> float:
        return sum(l) / len(l)

    def should_buy(self, prices: List[float]) -> bool:
        return prices[-1] < self.list_average(prices)

    def should_sell(self, prices: List[float]) -> bool:
        return prices[-1] > self.list_average(prices)


class MinMaxTrader(TradingBot):
    def should_buy(self, prices: List[float]) -> bool:
        return return prices[-1] == min(prices)

    def should_sell(self, prices: List[float]) -> bool:
        return return prices[-1] == max(prices)

application = MinMaxTrader()
application.check_prices("BTC/USD")
application2 = AverageTrader()
application2.check_prices("BTC/USD")


################################################################################
# CODE AFTER applying bridge desing class
################################################################################

## Bridge solves is that it gives you cap of adding extra classes connected,
## is mechanism to have 2 separated classes that can change independently
## from each other.

## We now have a structure were we can have diferent exchanges and different
## strategies.
from typing import List
from abc import ABC, abstractmethod


class Exchange(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_market_data(self, coin: str) -> List[float]:
        pass

class Binance(Exchange):
    def connect(self):
        print(f"Connecting to Binance exchange...")

    def get_market_data(self, coin: str) -> List[float]:
        return [10, 12, 18, 14]

class Coinbase(Exchange):
    def connect(self):
        print(f"Connecting to Coinbase exchange...")

    def get_market_data(self, coin: str) -> List[float]:
        return [10, 12, 18, 20]


class TradingBot(ABC):
    def __init__(self, exchange: Exchange):
        self.exchange = exchange

    @abstractmethod
    def should_buy(self, prices: List[float]) -> bool:
        pass

    @abstractmethod
    def should_sell(self, prices: List[float]) -> bool:
        pass

    def check_prices(self, coin: str):
        self.connect()
        prices = self.get_market_data(coin)
        should_buy = self.should_buy(prices)
        should_sell = self.should_sell(prices)
        if should_buy:
            print(f"You should buy {coin}!")
        elif should_sell:
            print(f"You should sell {coin}!")
        else:
            print(f"No action needed for {coin}.")


application = MinMaxTrader(Coinbase())
application.check_prices("BTC/USD")
application = MinMaxTrader(Binance())
application.check_prices("BTC/USD")
