class Edge:

    def __init__(self, tickerInfo, fromNodeId, toNodeId, rate):
        self.tickerInfo = tickerInfo
        self.fromNodeId = fromNodeId
        self.toNodeId = toNodeId
        self.id = fromNodeId + toNodeId
        self.rate = rate
        self.fee = 0.001

    def __str__(self):
        return "From " + self.fromNodeId + ", to " + self.toNodeId + " with rate " + str(self.rate)

    def makeTrade(self, units):
        feeAmount = units * self.fee
        unitsAfterFee = units - feeAmount
        return unitsAfterFee * self.rate


class TickerInfo:

    def __init__(self, symbol, buy):
        self.symbol = symbol
        self.buy = buy

    def __str__(self):
        return "Ticker " + self.symbol + " where buy is " + str(self.buy)
