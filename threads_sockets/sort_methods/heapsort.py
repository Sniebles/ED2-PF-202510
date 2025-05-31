
def heapsort(data, key):
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, key)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        heapify(data, i, 0, key)

def heapify(data, heap_size, root_index, key):
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
