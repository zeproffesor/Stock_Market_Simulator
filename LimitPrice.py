from Queue import Queue

class LimitPrice:
    def __init__(self, limit_price):
        self.price = limit_price # int (for now) 
        self.order_queues = ( Queue(), Queue() ) # ( sell order queue, buy order queue )
        self.order_hashMap = dict() # O(1) order access

    def __str__(self):
        ret = ""
        for order_id in self.order_hashMap:
            if self.order_hashMap[order_id].direction:
                ret += str(self.order_hashMap[order_id])+"\n"
        for order_id in self.order_hashMap:
            if not (self.order_hashMap[order_id].direction):
                ret += str(self.order_hashMap[order_id])+"\n"
        return ret
    
    def oldest_order(self, direction):
        return self.order_queues[direction].front()

    def num_orders(self, direction):
        return self.order_queues[direction].size()

    def add_order(self, order):
        self.order_queues[order.direction].push(order)
        self.order_hashMap[order.id] = order

    def cancel_order(self, order):
        self.order_queues[order.direction].remove(order)
        del self.order_hashMap[order.id]