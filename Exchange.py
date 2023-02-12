import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


class Exchange:
    def __init__(self, host, port):
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((host, port))
        self.lsock.listen()
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
                print(data.outb)
            else:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()

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


# def main():
#     if len(sys.argv) != 3:
#         print(f"Usage: {sys.argv[0]} <host> <port>")
#         sys.exit(1)

#     host, port = sys.argv[1], int(sys.argv[2])
#     exchange = Exchange(host,port)
#     exchange.work()

# main()