def quicksort(data, low, high, key):
    if low < high:
        pivot_index = partition(data, low, high, key)
        quicksort(data, low, pivot_index - 1, key)
        quicksort(data, pivot_index + 1, high, key)

def partition(data, low, high, key):
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


