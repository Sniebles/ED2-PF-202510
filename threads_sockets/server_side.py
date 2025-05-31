import socket
import threading
import struct

sortMethods = ['CubeSort','QuickSort', 'MergeSort', 'HeapSort']
count = 0

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        print("server side:\n----New connection added: ", clientAddress)

    def run(self):
        global count

        print("server side:\n----Connection from : ", self.clientAddress)
        msg = ''
        data = self.csocket.recv(2048)
        msg = data.decode()
        print("server side:\n----from client:", msg)

        self.csocket.send(bytes(sortMethods[count], 'UTF-8'))
        count += 1

        def recv_exact(sock, n):
            data = b''
            while len(data) < n:
                more = sock.recv(n - len(data))
                if not more:
                    raise ConnectionError("Conexión cerrada antes de recibir todos los datos")
                data += more
            return data

        time = 0.0
        data = recv_exact(self.csocket, 4)
        time = struct.unpack('f', data)[0]
        
        print("server side:\n----Time taken by ", sortMethods[count - 1], " is ", time, " seconds")

        print("server side:\n----Client at ", self.clientAddress, " disconnected")


def start_server():
    LOCALHOST = "192.168.1.9"
    PORT = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("server side:\n----Server started")
    print("server side:\n----Waiting for client request..")
    while count < len(sortMethods):
        server.listen(len(sortMethods))
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()
        if count == len(sortMethods):
            print("server side:\n----All sort methods have been sent.")
