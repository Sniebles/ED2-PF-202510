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


def run_algorithm(alg_name: str, MAX_RUNS=1, seed_offset=0, sub_ind=None):
    table = tst.rr.read_csv("data files/data.csv")
    func = sortingFunction[alg_name]
    runs = 0
    while (runs < MAX_RUNS):
        recorded_time = [0.0]
        print(f'{runs+seed_offset}-{alg_name} about to start')
        tst.run_and_time(alg_name, func, table, "CANTIDAD", returnedTime=recorded_time,random_seed=runs+seed_offset,shouldCopy=False)
        if sub_ind is None:
            sortingTimes[alg_name].append(recorded_time[0])
        else:
            sortingTimes[alg_name][sub_ind].append(recorded_time[0])
            
            
        runs += 1
    
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    if sub_ind is None:
        filename = os.path.join(base_directory, "data files", "results2", f"{alg_name}.csv")    
        make_folder(filename)
        with open(filename, "w", newline="") as out:
            writer = csv.writer(out)
            writer.writerow(outputHeader)
            for t in sortingTimes[alg_name]:
                writer.writerow([alg_name, t])
    else:
        filename = os.path.join(base_directory, "data files", "results2", f"{alg_name}-{sub_ind}.csv")    
        make_folder(filename)
        with open(filename, "w", newline="") as out:
            writer = csv.writer(out)
            writer.writerow(outputHeader)
            for t in sortingTimes[alg_name][sub_ind]:
                writer.writerow([alg_name, t])



if __name__ == "__main__":
    print("Program Started")
    pool = Pool(processes=4)
    start = time.time()
    r1 = pool.apply_async(run_algorithm, ["CubeSort", 3,])
    r2 = pool.apply_async(run_algorithm, ["QuickSort", 3,])
    r3 = pool.apply_async(run_algorithm, ["MergeSort", 3,])
    r4 = pool.apply_async(run_algorithm, ["HeapSort", 3,])
    
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