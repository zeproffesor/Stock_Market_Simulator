from Mappings import name_to_id

class Order:
    unq_id = 0
    def __init__(self, player_id, direction, stock_name, limit_price):
        self.player_id = player_id # int
        self.direction = direction # 1 (buy) or 0 (sell)
        self.stock_id = name_to_id[stock_name] # int stock id
        # self.qty = qty # int
        self.limit_price = limit_price # float
        self.id = Order.unq_id
        Order.unq_id += 1
