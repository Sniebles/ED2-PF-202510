import sql_connection as sc
from sort_methods import test as t
import client_side as c
import server_side as s
import threading as th

MAX_RUNS = 1
if __name__ == '__main__':
    print("Saving data to files...\n-------------------------------\n")
    # sc.save_data_to_files()
    print("\nData saved to files successfully.\n")

    # print("Running threading tests with: (CubeSort, Quicksort, Mergesort, Heapsort)\n-------------------------------\n")
    t.test()
    print("\nAll sort methods completed successfully.")
    # print("Threading tests completed successfully.\n")
    
    print("Starting server and clients: (CubeSort, Quicksort, Mergesort, Heapsort)...\n-------------------------------\n")
    
    server_th = th.Thread(target=s.start_server, args=(MAX_RUNS,))
    
    clients_th = []
    table = t.rr.read_csv("data files/data.csv")
    for _ in range(4):
        clients_th.append(th.Thread(target=c.run_client, args=(table, MAX_RUNS,)))
    
    server_th.start()

    s.server_started.wait()

    for client in clients_th:
        client.start()

    server_th.join()
    for client in clients_th:
        client.join()
    print("\nAll sort methods completed successfully.")
    print("Server and clients completed successfully.\n")

    print("All tests completed successfully.\n")
    print("End of threading and sockets tests.\n")