import socket
import threading
import struct
import os
import csv
from sql_connection import make_folder
sortMethods = ['CubeSort','QuickSort', 'MergeSort', 'HeapSort']
count = 0
count_lock = threading.Lock()
clients_count = 0
sortingTimes = {
    'CubeSort': [],
    'QuickSort': [],
    'MergeSort': [],
    'HeapSort': []
}
outputHeader = ["Algorithm", "Runtime"]


server_started = threading.Event()

class ClientThread(threading.Thread):
    """
    A class that handles communication to and from a client socket. Assigns client socket an
    algorithm and waits for it to report its recorded runtime before writing it to a file.
    """
    def __init__(self, clientAddress, clientsocket: socket.socket, MAX_RUNS:int=1):
        """
        Parameters:
            clientAddress:
            clientsocket:
            MAX_RUNS (int, optional): Number of times to wait for a runtime response before writing to file
        Returns:
            None
        """
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        self.MAX_RUNS = MAX_RUNS
        self.runs = 0
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
        
        while self.runs < self.MAX_RUNS:
            time = 0.0
            data = recv_exact(self.csocket, 4)
            time = struct.unpack('f', data)[0]

            print("server side:--------------------------Time taken by ", sortMethods[c], " is ", time, " seconds")

            sortingTimes[sortMethods[c]].append(time)
            self.runs += 1

        print("server side:--------------------------Client at ", self.clientAddress, " disconnected")
        
        base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        filename = os.path.join(base_directory, "data files", "results", f"{sortMethods[c]}.csv")
        make_folder(filename)
        with open(filename, "w", newline="") as out:
            writer = csv.writer(out)
            writer.writerow(outputHeader)
            for t in sortingTimes[sortMethods[c]]:
                writer.writerow([sortMethods[c], t])


def start_server(MAX_RUNS:int=1):
    """
    Starts server socket and listens for connections from clients to create a handling thread.
    Parameters:
        MAX_RUNS (int, optional): Number of times to wait for a runtime response in each handling thread.
    """
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
        newthread = ClientThread(clientAddress, clientsock, MAX_RUNS)
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
