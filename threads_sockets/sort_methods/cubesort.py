def cube_sort(data: list, key: str):
    """
    Custom cube sort implementation for dictionary lists that splits input data into buckets according to the range each
    item falls in and sorts them via insertion sort.
    Parameters:
        data (list): Dictionary list to sort
        key (str): Key to sort dictionaries by
    """
    if not data: 
        return

    mn = min(int(x[key]) for x in data)
    mx = max(int(x[key]) for x in data)

    n = len(data)
    bucket_count = max(1, n // 10)
    tamaño_rango = (mx - mn + 1) / bucket_count

    buckets = [[] for _ in range(bucket_count)]
    for x in data:
        idx = int((int(x[key]) - mn) / tamaño_rango)
        if idx == bucket_count:
            idx -= 1
        buckets[idx].append(x)

    for b in buckets:
        for i in range(1, len(b)):
            temp = b[i]
            j = i - 1
            while j >= 0 and int(b[j][key]) > int(temp[key]):
                b[j + 1] = b[j]
                j -= 1
            b[j + 1] = temp

    k = 0
    for b in buckets:
        for x in b:
            data[k] = x
            k += 1