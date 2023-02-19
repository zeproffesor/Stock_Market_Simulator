from Order import Order

class OrderNode:
    def __init__(self, order=None):
        self.order = order
        self.next_order = None
        self.prev_order = None

class LimitPrice:
    def __init__(self, limit_price):
        self.price = limit_price # float 
        self.order_lists = ( [OrderNode(), None] , [OrderNode(), None] ) # ( [sell head, sell tail], [buy head, buy tail] )
        self.order_lists[0][1], self.order_lists[1][1] = self.order_lists[0][0], self.order_lists[1][0] 
        self.order_hashMap = dict() # O(1) order access

    def add_order(self, order):
        order_node = OrderNode(order)
        tail = self.order_lists[order.direction][1]
        head = self.order_lists[order.direction][0]
        if tail != head:
            tail.next_order = order_node
            order_node.prev_order = tail
        else:
            head.next_order = order_node
            order_node.prev_order = head
        self.order_lists[order.direction][1] = order_node
        self.order_hashMap[order.id] = order_node

    def cancel_order(self, order):
        order_node = self.order_hashMap[order.id]
        prev_node = order_node.prev_order
        next_node = order_node.next_order
        prev_node.next_order = next_node
        if next_node:
            next_node.prev_order = prev_node
        else:
            self.order_lists[order.direction][1] = order_node.prev_order
        del self.order_hashMap[order.id]

