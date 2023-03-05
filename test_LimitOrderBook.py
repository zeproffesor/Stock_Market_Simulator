from unittest import TestCase, main
from LimitOrderBook import LimitOrderBook
from Order import Order

class LimitOrderBookTest(TestCase):

    def test_str(self):
        lob = LimitOrderBook()
        order = Order(1,1,'AAPL',200)
        lob.add_order(order)
        self.assertEqual("1,200\n",lob.__str__())

    def test_add_order(self):
        lob = LimitOrderBook()
        order = Order(1,1,'AAPL',200)
        lob.add_order(order)

        self.assertEqual(lob.book[200].oldest_order(1), order)
        self.assertEqual(lob.book[200].num_orders(1), 1)

    def test_cancel_order(self):
        lob = LimitOrderBook()
        order = Order(1,1,'AAPL',200)
        lob.add_order(order)

        self.assertEqual(lob.book[200].oldest_order(1), order)
        self.assertEqual(lob.book[200].num_orders(1), 1)

        lob.cancel_order(order)

        self.assertEqual(lob.book[200].oldest_order(1), None)
        self.assertEqual(lob.book[200].num_orders(1), 0)

    def test_match_order(self):
        lob = LimitOrderBook()
        order1 = Order(1,1,'AAPL',200)
        lob.add_order(order1)

        self.assertEqual(lob.book[200].oldest_order(1), order1)
        self.assertEqual(lob.book[200].num_orders(1), 1)

        order2 = Order(2,0,'AAPL',198)
        lob.add_order(order2)

        self.assertEqual(lob.book[198].oldest_order(0), order2)
        self.assertEqual(lob.book[198].num_orders(0), 1)

        matched_order = lob.match_order(order2)

        self.assertEqual(matched_order, order1)
        self.assertEqual(lob.book[200].num_orders(1), 0)
        self.assertEqual(lob.book[198].num_orders(0), 0)

if __name__ == '__main__':
    main()