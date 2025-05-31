import socket
import struct

from sort_methods import test as t
from sort_methods import quicksort as qs
from sort_methods import cubesort as cs
from sort_methods import mergesort as ms
from sort_methods import heapsort as hs

def run_client():
    """Connects to the server, requests a sorting method, and sends back the time taken for sorting.
    The server will respond with the sorting method to use, and the client will execute the sorting
    method on a predefined dataset, measuring the time taken for the sort.
    """

    SERVER = "192.168.1.9"
    PORT = 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    client.sendall(bytes("Waiting for server response...", 'UTF-8'))

    data = ""
    response = client.recv(2048)
    data = response.decode()
    print("client side:\n----Received from server:", data)

    func = cs.cube_sort
    if data.lower() == "quicksort":
        func = qs.quicksort
    elif data.lower() == "mergesort":
        func = ms.mergesort
    elif data.lower() == "heapsort":
        func = hs.heapsort

    time = [0.0]

    t.run_and_time(data, func, t.rr.read_csv("data files/data.csv"), "CANTIDAD", returnedTime=time)
    client.sendall(struct.pack('f', time[0]))

    client.close()
