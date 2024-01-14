from datetime import datetime, timedelta

import backtrader as bt
import yfinance as yf

cerebro = bt.Cerebro()

start_date = datetime(2018, 3, 1)
end_date = datetime(2020, 7, 25)

dates = []


# Create a Stratey
class strategy(bt.Strategy):

    def log(self, txt, dt=None):
        # Logging function for this strategy
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.stopping = False
        self.dataclose = self.datas[0].close
        self.total = 0
        self.threshold = 0

    # Sehr nervig hier weil die Daten von Yahoo nicht komplett sind und man das näheste datum finden muss, SEHRRR NERVIG
    def next(self):
        # sell before data ends and stop graphing
        if self.datas[0].datetime.date(0) == (end_date - timedelta(days=2)).date() or self.stopping:
            for i in range(self.total):
                self.sell(self.datas[0])

            self.stopping = True
            return

        day1 = self.datas[0].datetime.date(0).strftime("%y") + self.datas[0].datetime.date(0).strftime("%j")
        day2 = self.datas[0].datetime.date(1).strftime("%y") + self.datas[0].datetime.date(1).strftime("%j")

        for date in dates:
            cur_day = date['date'].date().strftime("%y") + date['date'].date().strftime("%j")

            if int(day1) <= int(cur_day) < int(day2):
                if date['sentiment'] == 'POS':
                    self.buy(self.datas[0])
                    self.threshold = self.dataclose[0]
                    self.total += 1
                elif date['sentiment'] == 'NEG' and self.total > 0 and self.threshold < self.dataclose[0]:
                    self.sell(self.datas[0])
                    self.total -= 1


def add_date(date: datetime, sentiment: str):
    dates.append({"date": date, "sentiment": sentiment})


def run(ticker):
    # Create a Data Feed
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start_date, end_date))

    cerebro.adddata(data)
    cerebro.addstrategy(strategy)

    cerebro.run()
    cerebro.plot()


