import socket as sk
import threading as th

server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(('localhost', 10000))

while True:
    server.listen(5)
    clientsock, adrr = server.accept()
    print("hi! ", adrr)
    def handle_client(clientsock):
        while True:
            in_data = clientsock.recv(1024)
            if not in_data:
                break
            print("From Client:", in_data.decode())
            out_data = input("Reply to Client: ")
            clientsock.sendall(bytes(out_data, 'UTF-8'))
            if out_data.lower() == 'bye':
                break
        clientsock.close()
    clientsock.sendall(bytes("Hello from Server", 'UTF-8'))
    clientsock.close()