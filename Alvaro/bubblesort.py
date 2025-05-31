def bubblesort(data, key):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if int(data[j][key]) > int(data[j + 1][key]):
                data[j], data[j + 1] = data[j + 1], data[j]

