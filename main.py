import selectors
import socket


selector = selectors.DefaultSelector()


def server():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(("localhost", 1234))
    serv.listen()

    selector.register(fileobj=serv, events=selectors.EVENT_READ, data=accept_con)



def accept_con(serv):
    client, adr = serv.accept()
    selector.register(fileobj=client, events=selectors.EVENT_READ, data=msg)


def msg(client):
    rq = client.recv(4090)

    if rq:
        res = "hello\n".encode()
        client.send(res)
    else:
        selector.unregister(client)
        client.close()


def event_loop():
    while 1:
        events = selector.select()

        for key, _ in events:
            c = key.data
            c(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
