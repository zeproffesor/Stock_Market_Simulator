from unittest import TestCase, main
from LimitOrderBook import LimitPrice
from Order import Order

class LimitPriceTest(TestCase):

    def test_init(self):
        lp = LimitPrice(215.5)
        self.assertEqual(lp.price, 215.5)
        self.assertEqual(lp.order_lists[0][0], lp.order_lists[0][1])
        self.assertEqual(lp.order_lists[1][0], lp.order_lists[1][1])

    def test_add_order(self):
        lp = LimitPrice(200.0)

        order1 = Order(1, 0, 'AAPL', 1, 200.0)
        lp.add_order(order1)
        order1_node = lp.order_hashMap[order1.id]

        self.assertNotEqual(lp.order_lists[0][0], lp.order_lists[0][1])
        self.assertEqual(lp.order_lists[1][0], lp.order_lists[1][1])

        sell_head = lp.order_lists[0][0]
        sell_tail = lp.order_lists[0][1]

        self.assertEqual(sell_head.next_order, sell_tail)
        self.assertEqual(order1,sell_tail.order)

        order2 = Order(2, 0, 'AAPL', 1, 200.0)
        lp.add_order(order2)
        order2_node = lp.order_hashMap[order2.id]

        sell_head = lp.order_lists[0][0]
        sell_tail = lp.order_lists[0][1]
        
        self.assertEqual(sell_tail, order2_node)
        self.assertEqual(sell_tail, order1_node.next_order)
        self.assertEqual(sell_tail.prev_order, order1_node)
        self.assertEqual(sell_head, order1_node.prev_order)
        self.assertEqual(order1_node.next_order, order2_node)
        self.assertEqual(order1_node, order2_node.prev_order)

    def test_cancel_order(self):
        lp = LimitPrice(200.0)

        order1 = Order(1, 0, 'AAPL', 1, 200.0)
        lp.add_order(order1)
        order1_node = lp.order_hashMap[order1.id]

        order2 = Order(2, 0, 'AAPL', 1, 200.0)
        lp.add_order(order2)
        order2_node = lp.order_hashMap[order2.id]

        order3 = Order(3, 0, 'AAPL', 1, 200.0)
        lp.add_order(order3)
        order3_node = lp.order_hashMap[order3.id]

        sell_head = lp.order_lists[0][0]
        sell_tail = lp.order_lists[0][1]

        self.assertEqual(sell_tail, order3_node)
        self.assertEqual(sell_tail.prev_order, order2_node)
        self.assertEqual(order2_node.prev_order, order1_node)
        self.assertEqual(sell_head.next_order, order1_node)

        lp.cancel_order(order2)
        sell_head = lp.order_lists[0][0]
        sell_tail = lp.order_lists[0][1]

        self.assertEqual(sell_tail, order3_node)
        self.assertEqual(sell_tail.prev_order, order1_node)
        self.assertEqual(sell_head.next_order, order1_node)

        lp.cancel_order(order3)
        sell_head = lp.order_lists[0][0]
        sell_tail = lp.order_lists[0][1]

        self.assertEqual(sell_tail, order1_node)
        self.assertEqual(sell_tail.prev_order, sell_head)
        self.assertEqual(sell_head.next_order, order1_node)

        lp.cancel_order(order1)
        sell_head = lp.order_lists[0][0]
        sell_tail = lp.order_lists[0][1]
        self.assertEqual(sell_tail, sell_head)

        

if __name__ == '__main__':
    main()