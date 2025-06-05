def quicksort(data: list, low: int, high:int, key:str):
    """
    Quicksort implementation to sort dictionary lists using the provided key
    Parameters:
        data (list): Dictionary list
        low (int): Lower index bound
        high (int): Higher index bound
        key (str): Key to sort dictionaries by
    """
    if low < high:
        pivot_index = partition(data, low, high, key)
        quicksort(data, low, pivot_index - 1, key)
        quicksort(data, pivot_index + 1, high, key)

def partition(data: list, low: int, high:int, key: str):
    """
    Returns pivot index for a quicksort partition after exchanging the necessary items
    """
    pivot = int(data[(low + high) // 2][key])
    i = low
    j = high

    while i <= j:
        while int(data[i][key]) < pivot:
            i += 1
        while int(data[j][key]) > pivot:
            j -= 1
        if i <= j:
            data[i], data[j] = data[j], data[i]
            i += 1
            j -= 1
    return i - 1


