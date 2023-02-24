from unittest import TestCase, main
from LimitPrice import LimitPrice
from Order import Order

class LimitPriceTest(TestCase):

    def test_init(self):
        lp = LimitPrice(215.5)
        self.assertEqual(lp.price, 215.5)
        self.assertEqual(lp.num_orders(0),0)
        self.assertEqual(lp.num_orders(1),0)
        self.assertEqual(lp.oldest_order(0), None)
        self.assertEqual(lp.oldest_order(1), None)

    def test_add_order(self):
        lp = LimitPrice(200.0)

        order1 = Order(1, 0, 'AAPL', 200.0)
        lp.add_order(order1)
        order1_cached = lp.order_hashMap[order1.id]

        self.assertEqual(order1_cached, order1)
        self.assertEqual(order1_cached, lp.oldest_order(0))
        self.assertEqual(1, lp.num_orders(0))

        order2 = Order(2, 0, 'AAPL', 200.0)
        lp.add_order(order2)
        order2_cached = lp.order_hashMap[order2.id]
        
        self.assertEqual(lp.num_orders(0),2)
        self.assertEqual(order1_cached, lp.oldest_order(0))
        self.assertEqual(order1, lp.oldest_order(0))
        lp.cancel_order(order1)
        self.assertEqual(lp.num_orders(0),1)
        self.assertEqual(order2, lp.oldest_order(0))
        self.assertEqual(order2_cached, lp.oldest_order(0))
        

    def test_cancel_order(self):
        lp = LimitPrice(200.0)

        order1 = Order(1, 1, 'AAPL', 200.0)
        lp.add_order(order1)
        order1_cached = lp.order_hashMap[order1.id]

        order2 = Order(2, 1, 'AAPL', 200.0)
        lp.add_order(order2)
        order2_cached = lp.order_hashMap[order2.id]

        order3 = Order(3, 1, 'AAPL', 200.0)
        lp.add_order(order3)
        order3_cached = lp.order_hashMap[order3.id]

        orders = [order1_cached, order2_cached, order3_cached]
        i = 0
        while lp.num_orders(1):
            self.assertEqual(orders[i], lp.oldest_order(1))
            lp.cancel_order(orders[i])
            i += 1
        self.assertEqual(0, lp.num_orders(1))

        

if __name__ == '__main__':
    main()