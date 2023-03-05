import sys
import socket
import selectors
import types
from Order import Order
from LimitOrderBook import LimitOrderBook

sel = selectors.DefaultSelector()

DELTA = 3.0

class Exchange:
    def __init__(self, host, port):
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.book = LimitOrderBook()
        self.lsock.bind((host, port))
        self.lsock.listen(10)
        print(f"Listening on {(host, port)}")
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Acking order {data.outb!r} to Player {data.addr}")
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                order = self.parse_order(data.outb)
                self.book.add_order(order)
                self.book.match_order(order)
            else:
                state = []
                book = self.book.__str__().split("\n")
                for ord in book:
                    if not len(ord):
                        continue
                    dir, price = ord.split(',')[0],ord.split(',')[1] 
                    state.append((int(dir),int(price)))
                self.visualise(state)
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()

    def parse_order(self, order):
        args = order.decode().split(',')
        args[0] = int(args[0])
        args[1] = int(args[1])
        args[3] = int(args[3])
        return Order(*args)
    
    def visualise(self, state):
        buy_orders = []
        sell_orders = []
        for ord in state:
            if ord[0]==0:
                sell_orders.append(ord[1])
            else:
                buy_orders.append(ord[1])
        buy_orders.sort()
        sell_orders.sort()
        hist = ["" for _ in range(10001)]
        for price in buy_orders:
            hist[price] += '#'
        for price in sell_orders:
            hist[price] += '*'
        i=0
        while i<len(hist):
            if len(hist[i])>0:
                print(hist[i])
                i+=1
            else:
                print('.')
                while i<len(hist) and len(hist[i])==0:
                    i+=1
        print('\n')

    def work(self):
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting")
        finally:
            self.sel.close()


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    exchange = Exchange(host,port)
    exchange.work()

main()