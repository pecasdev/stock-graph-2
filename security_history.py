from datetime import datetime


class SecurityHistory:
    def __init__(self):
        # history[datetime] = (share_count, total_share_cost)
        self.history = {}
        self.share_count = 0
        self.total_share_cost = 0

    # get the most recent history state that occured before or at a datetime
    def last_entry_before_or_at_datetime(self, datetime: "datetime"):
        for k in sorted(self.history.keys(), reverse=True):
            if k <= datetime:
                return self.history[k]

    def buy(self, datetime: "datetime", price: float, count: int):
        self.total_share_cost += price * count
        self.share_count += count

        self.history[datetime] = (self.share_count, self.total_share_cost)

    def sell(self, datetime: "datetime", price: float, count: int):
        self.buy(datetime, price, -count)

    def __repr__(self):
        return str(self.history)

    def __str__(self):
        return self.__repr__()