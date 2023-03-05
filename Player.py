import sys
import socket
import selectors
import types
from matplotlib import pyplot
import numpy
from IPython.display import clear_output


ALPHA = 5.0
MU = 5.0
DELTA = 3.0

class Player:
    def __init__(self):
        self.sel = selectors.DefaultSelector()

    def start_connection(self, host, port, order):
        server_addr = (host, port)
        print(f"Starting connection to Exchange at {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            msg_total=len(order),
            recv_data = b"",
            messages=order,
            outb=b"",
        )
        self.sel.register(sock, events, data=data)
    
    def generate_orders(self):
        num_market_orders = numpy.random.poisson(MU)
        num_limit_orders = numpy.random.poisson(ALPHA)
        num_cancel_orders = numpy.random.poisson(DELTA)

        ret = []
        for _ in range(num_market_orders):
            order = "1 "
            dir = numpy.random.randint(0,2)
            order += str(dir)+" "
            order += "AAPL "
            order += "10000 " if dir else "0 "
            ret.append(order)
        
        for _ in range(num_limit_orders):
            order = "1 "
            dir = numpy.random.randint(0,2)
            order += str(dir)+" "
            order += "AAPL "
            price = numpy.random.randint(0,10001)
            order += str(price)+" "
            ret.append(order)

        cancel_orders = list(numpy.random.choice(numpy.array(self.curr_orders), num_cancel_orders))
        ret.extend(cancel_orders)
        return ret

    def place_order(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages
                data.messages = b""
            while len(data.outb):
                print(f"Sending order {data.outb!r} to exchange")
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
            while 1:
                events = self.sel.select(timeout=1)
                for key,mask in events:
                    if not (mask & selectors.EVENT_READ):
                        continue
                    else:
                        self.recv_ack(key,mask)
                if not self.sel.get_map():
                    break
        else:
            print(f"Error in sending order! Closing connection...")
            self.sel.unregister(sock)
            sock.close()

    def recv_ack(self, key,mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.recv_data += recv_data
            if not recv_data or len(data.recv_data) == (data.msg_total):
                print(f"Received ack for {data.recv_data!r} from Exchange")
                print(f"Order placed! Closing connection to exchange...")
                self.sel.unregister(sock)
                sock.close()

    # Can be used for passing custom orders
    def play(self, host, port):
        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.place_order(key, mask)
                # Example order = "1, 0, AAPL, 100"
                order = input("Place order:")
                order = bytes(order,'utf-8')
                self.start_connection(host, int(port), order)
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting")
        finally:
            self.sel.close()

    # def play(self, host, port):
    #     try:
    #         while True:
    #             events = self.sel.select(timeout=1)
    #             if events:
    #                 for key, mask in events:
    #                     self.place_order(key, mask)
    #             # Example order = "1, 0, AAPL, 100"
    #             orders = self.generate_orders()
    #             for order in orders:
    #                 self.start_connection(host, int(port), order)
    #             if not self.sel.get_map():
    #                 break
    #     except KeyboardInterrupt:
    #         print("\nCaught keyboard interrupt, exiting")
    #     finally:
    #         self.sel.close()

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host, port = sys.argv[1:3]
    player = Player()
    player.play(host,port)


main()