def heapsort(data: list, key: str):
    """
    Heapsort implementation for dictionary lists using the provided key for comparisons
    Parameters:
        data (list): Dictionary list
        key (str): Key to sort by
    """
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, key)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        heapify(data, i, 0, key)

def heapify(data: list, heap_size: int, root_index: int, key: str):
    """
    Creates a max heap assuming the provided array is mostly already sorted, only checking the provided index
    and recursing on the child it gets swapped with if out of place.
    Parameters:
        data (list): Dictionary list to build max heap from
        heap_size (int): Size of the list
        root_index (int): List index of the root
        key (str): Key to sort dictionaries by
    """
    largest = root_index
    left = 2 * root_index + 1
    right = 2 * root_index + 2

    def value(idx):
        return int(data[idx][key])

    if left < heap_size and value(left) > value(largest):
        largest = left
    if right < heap_size and value(right) > value(largest):
        largest = right
    if largest != root_index:
        data[root_index], data[largest] = data[largest], data[root_index]
        heapify(data, heap_size, largest, key)
