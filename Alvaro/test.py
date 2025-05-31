import copy
import os
import time
import read_record as rr
import threading as t
import bubblesort as bs
import quicksort as qs
import mergesort as ms
import heapsort as hs

# Execute & record time
def run_and_time(name, func, data, key):
    arr = copy.deepcopy(data)
    start = time.time()
    if name.lower() == 'quicksort':
        func(arr, 0, len(arr) - 1, key)
    else:
        func(arr, key)
    end = time.time()
    print(f"{name} ended in {end - start:.6f} seconds")


def main():
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    entry_route = os.path.join(base_directory, "data files", "data.csv")
    exit_route = os.path.join(base_directory, "data files", "data_sorted.csv")
    sort_column = "CANTIDAD"

    data = rr.read_csv(entry_route)

    threads = [
        t.Thread(target=run_and_time, args=("BubbleSort", bs.bubblesort, data, sort_column)),
        t.Thread(target=run_and_time, args=("QuickSort", qs.quicksort, data, sort_column)),
        t.Thread(target=run_and_time, args=("MergeSort", ms.mergesort, data, sort_column)),
        t.Thread(target=run_and_time, args=("HeapSort", hs.heapsort, data, sort_column)),
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Guardar el ordenamiento de uno de los métodos (ejemplo: quicksort)
    sorted_data = copy.deepcopy(data)
    qs.quicksort(sorted_data, sort_column)
    rr.record_csv(exit_route, sorted_data, fields=sorted_data[0].keys())

    print("Sorted and recorded:", exit_route)
    print("All the algorithms are done.")

if __name__ == "__main__":
    main()





