import copy
import os
import random
import time
import sort_methods.read_record as rr
import threading as t
import sort_methods.cubesort as cs
import sort_methods.quicksort as qs
import sort_methods.mergesort as ms
import sort_methods.heapsort as hs
from typing import Callable
# Execute & record time
def run_and_time(name : str, func: Callable[[list, str], None], data:list, key:str, returnedTime:list=None, save_route:str=None, random_seed:int=None, shouldCopy:bool=True):
    """
    Parameters:
        -name (str): Algorithm name
        -func (Callable[[list, str], None]): Algorithm function reference
        -data (list): Database table to sort
        -key (str): Key to sort dictionary data by
        -returnedTime (list, optional): Single entry list to return algorithm runtime
        -save_route (str, optional): Filepath to save sorted list
        -random_seed (int, optional): Seed to shuffle data
        -shouldCopy (bool, optional): Whether a deepcopy should be made
    Returns:
        None
    """
    if shouldCopy:
        arr = copy.deepcopy(data)
    else:
        arr = data
        
    if random_seed:
        random.seed(random_seed)
        random.shuffle(arr)

    start = time.time()
    if name.lower() == 'quicksort':
        func(arr, 0, len(arr) - 1, key)
    else:
        func(arr, key)
    end = time.time()
    print(f"{name} ended in {end - start:.6f} seconds")
    if returnedTime is not None:
        returnedTime[0] = end - start
    if save_route is not None:
        rr.record_csv(save_route, arr, fields=arr[0].keys())
        print(f"Data saved to {save_route}")


def test():
    """
    Runs and times all 4 sorting algorithms in separate threads with input data read from ./data files/data.csv
    and writes the ordered lists to ./data files/data_sorted_{algorithm}.csv
    """
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    entry_route = os.path.join(base_directory, "data files", "data.csv")
    exit_routes = [
    os.path.join(base_directory, "data files", "data_sorted_" + method + ".csv") for method in ["CubeSort", "QuickSort", "MergeSort", "HeapSort"]
    ]
    sort_column = "CANTIDAD"

    print("Reading data from:", entry_route)
    data = rr.read_csv(entry_route)

    threads = [
        t.Thread(target=run_and_time, args=("CubeSort", cs.cube_sort, data, sort_column, None, exit_routes[0])),
        t.Thread(target=run_and_time, args=("QuickSort", qs.quicksort, data, sort_column, None, exit_routes[1])),
        t.Thread(target=run_and_time, args=("MergeSort", ms.mergesort, data, sort_column, None, exit_routes[2])),
        t.Thread(target=run_and_time, args=("HeapSort", hs.heapsort, data, sort_column, None, exit_routes[3])),
    ]

    print("Starting sorting algorithms in threads...\n")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    print("\nSorted and recorded")
    print("All the algorithms are done.")





