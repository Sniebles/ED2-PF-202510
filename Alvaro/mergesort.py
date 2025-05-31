def mergesort(data, key):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        mergesort(left_half, key)
        mergesort(right_half, key)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if int(left_half[i][key]) < int(right_half[j][key]):
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1

