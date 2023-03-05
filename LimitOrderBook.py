from LimitPrice import LimitPrice
from Queue import Queue


class LimitOrderBook:

    def __init__(self):
        self.book = [LimitPrice(x) for x in range(10001)] # Limit price book
    
    def __str__(self):
        ret = ""
        for lp in self.book:
            ret += str(lp)
        return ret

    def add_order(self, order):
        self.book[order.limit_price].add_order(order)
    
    def cancel_order(self, order):
        self.book[order.limit_price].cancel_order(order)

    def match_order(self, order):
        matched_order = None
        limit_price = 0 if order.direction else 10000
        while (limit_price<=order.limit_price if order.direction else limit_price>=order.limit_price):
            if self.book[limit_price].oldest_order(1-order.direction):
                matched_order = self.book[limit_price].oldest_order(1-order.direction)
                self.book[limit_price].cancel_order(matched_order)
                self.book[order.limit_price].cancel_order(order)
                break
            limit_price += 1 if order.direction else -1
        return matched_order