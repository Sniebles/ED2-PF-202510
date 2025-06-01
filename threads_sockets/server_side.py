import socket
import threading
import struct

sortMethods = ['CubeSort','QuickSort', 'MergeSort', 'HeapSort']
count = 0
count_lock = threading.Lock()
clients_count = 0
sortingTimes = {
    'CubeSort': 0.0,
    'QuickSort': 0.0,
    'MergeSort': 0.0,
    'HeapSort': 0.0
}
server_started = threading.Event()

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        print("server side:--------------------------New connection added: ", clientAddress)

    def run(self):
        global count

        print("server side:--------------------------Connection from : ", self.clientAddress)
        msg = ''
        data = self.csocket.recv(2048)
        msg = data.decode()
        print("server side:--------------------------from client:", msg)

        with count_lock:
            c = count
            count += 1
            
        self.csocket.send(bytes(sortMethods[c], 'UTF-8'))

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
        
        print("server side:--------------------------Time taken by ", sortMethods[c], " is ", time, " seconds")

        sortingTimes[sortMethods[c]] = time

        print("server side:--------------------------Client at ", self.clientAddress, " disconnected")


def start_server():
    #LOCALHOST = "192.168.1.9"
    PORT = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', PORT))
    server_started.set()
    print("server side:--------------------------Server started")
    print("server side:--------------------------Waiting for client requests..")
    global clients_count
    threads = []
    server.listen(len(sortMethods))
    while clients_count < len(sortMethods):
        clientsock, clientAddress = server.accept()
        clients_count += 1
        newthread = ClientThread(clientAddress, clientsock)
        threads.append(newthread)
        newthread.start()
        print("server side:--------------------------", clients_count, "sort methods sent so far.")
        if clients_count == len(sortMethods):
            print("server side:--------------------------All sort methods have been sent.")
    for t in threads:
        t.join()
    print("server side:--------------------------Server shutting down.")
    server.close()
    print("\nserver side:--------------------------Final sorting times:", sortingTimes)
