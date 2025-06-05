import socket
import struct
import time

from sort_methods import test as t
from sort_methods import quicksort as qs
from sort_methods import cubesort as cs
from sort_methods import mergesort as ms
from sort_methods import heapsort as hs

def run_client(table: list, MAX_RUNS:int=1):
    """Connects to the server, requests a sorting method, and sends back the time taken for sorting.
    The server will respond with the sorting method to use, and the client will execute the sorting
    method MAX_RUNS times on a shuffled predefined dataset, measuring the time taken for the sort.

    Parameters:
        -table (list): Database table as a list
        -MAX_RUNS (int, optional): Amount of times to run the sorting algorithm
    Returns:
        None
    """

    #SERVER = "192.168.1.9"
    PORT = 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', PORT))
    client.sendall(bytes("Waiting for server response...", 'UTF-8'))

    data = ""
    response = client.recv(2048)
    data = response.decode()
    print("client side:----Received from server:", data)

    func = cs.cube_sort
    if data.lower() == "quicksort":
        func = qs.quicksort
    elif data.lower() == "mergesort":
        func = ms.mergesort
    elif data.lower() == "heapsort":
        func = hs.heapsort
    
    runs = 0
    while (runs < MAX_RUNS):
        recorded_time = [0.0]
        t.run_and_time(data, func, table, "CANTIDAD", returnedTime=recorded_time,random_seed=runs)
        client.sendall(struct.pack('f', recorded_time[0]))
        runs += 1

    client.close()
