import os
import csv
import time
from sql_connection import make_folder
from multiprocessing import Pool
from threading import Thread

from sort_methods import test as tst
from sort_methods import quicksort as qs
from sort_methods import cubesort as cs
from sort_methods import mergesort as ms
from sort_methods import heapsort as hs

sortMethods = ['CubeSort','QuickSort', 'MergeSort', 'HeapSort']
sortingTimes = {
    'CubeSort': [],
    'QuickSort': [],
    'MergeSort': [],
    'HeapSort': []
}
sortingFunction = {
    'CubeSort': cs.cube_sort,
    'QuickSort': qs.quicksort,
    'MergeSort': ms.mergesort,
    'HeapSort': hs.heapsort
}
outputHeader = ["Algorithm", "Runtime"]


def run_algorithm(alg_name: str, MAX_RUNS:int=1, seed_offset:int=0, sub_ind:int=None):
    """
    Reads input table from a fixed location, runs the specified algorithm and records its runtime to a file
    Parameters:
        alg_name (str): Algorithm name
        MAX_RUNS (int, optional): How many times to run and time the algorithm
        seed_offset (int, optional): Data shuffling seed offset
        sub_ind (int, optional): If present, added to name of file results are written to, this allows using the same algorithm
            in multiple processes without having to worry about synchronization when writing results.
    """
    func = sortingFunction[alg_name]
    runs = 0
    while (runs < MAX_RUNS):
        table = tst.rr.read_csv("data files/data.csv")
        recorded_time = [0.0]
        print(f'{runs+seed_offset}-{alg_name} about to start')
        tst.run_and_time(alg_name, func, table, "CANTIDAD", returnedTime=recorded_time,random_seed=runs+seed_offset,shouldCopy=False)
        sortingTimes[alg_name].append(recorded_time[0])            
            
        runs += 1
    
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    if sub_ind is None:
        filename = os.path.join(base_directory, "data files", "results2", f"{alg_name}.csv")    
    else:
        filename = os.path.join(base_directory, "data files", "results2", f"{alg_name}-{sub_ind}.csv")    
    make_folder(filename)
    with open(filename, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(outputHeader)
        for t in sortingTimes[alg_name]:
            writer.writerow([alg_name, t])


if __name__ == "__main__":
    print("Program Started")
    pool = Pool(processes=4)
    start = time.time()
    r1 = pool.apply_async(run_algorithm, ["MergeSort", 25,0,0])
    r2 = pool.apply_async(run_algorithm, ["MergeSort", 25,25,1])
    r3 = pool.apply_async(run_algorithm, ["MergeSort", 25,50,2])
    r4 = pool.apply_async(run_algorithm, ["MergeSort", 25,75,3])
    
    pool.close()
    pool.join()
    print(f"Program finished in {time.time() - start:.6f} seconds")


'''if __name__ == "__main__": 
    print("Program Started")
    start = time.time()
    data_table = tst.rr.read_csv("data files/data.csv")
    print(f"Finished in {time.time() - start:.6f} seconds")
    print("Data read.")
    run_algorithm("CubeSort", data_table)
    #run_algorithm("QuickSort", data_table)
    #run_algorithm("MergeSort", data_table)
    #run_algorithm("HeapSort", data_table)
'''

'''if __name__ == "__main__":
    print("Program Started")
    data_table = tst.rr.read_csv("data files/data.csv")
    #run_algorithm("CubeSort", data_table)
    print("Data read.")
    t1 = Thread(target=run_algorithm, args=("CubeSort", data_table,))
    t3 = Thread(target=run_algorithm, args=("MergeSort", data_table,))
    t2 = Thread(target=run_algorithm, args=("QuickSort", data_table,))
    t4 = Thread(target=run_algorithm, args=("HeapSort", data_table,))
    start = time.time()
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print(f"Finished in {time.time() - start:.6f} seconds")'''
