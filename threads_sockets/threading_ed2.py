import sql_connection as sc
from sort_methods import test as t
import client_side as c
import server_side as s
import threading as th

if __name__ == '__main__':
    print("Saving data to files...\n-------------------------------\n")
    sc.save_data_to_files()
    print("\nData saved to files successfully.\n")

    print("Running threading tests with: (CubeSort, Quicksort, Mergesort, Heapsort)\n-------------------------------\n")
    t.test()
    print("\nAll sort methods completed successfully.")
    print("Threading tests completed successfully.\n")

    print("Starting server and clients: (CubeSort, Quicksort, Mergesort, Heapsort)...\n-------------------------------\n")
    
    th.Thread(target=s.start_server).start()
    for _ in range(4):
        th.Thread(target=c.run_client()).start()
    print("\nAll sort methods completed successfully.")
    print("Server and clients started successfully.\n")

    print("All tests completed successfully.\n")
    print("End of threading and sockets tests.\n")