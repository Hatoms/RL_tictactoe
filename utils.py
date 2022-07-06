def reorder(arr,index):

    SIZE_ARRAY = 9

    new_arr = [0] * SIZE_ARRAY;

    # arr[i] should be
        # present at index[i] index
    for i in range(SIZE_ARRAY):
        new_arr[index[i]] = arr[i]

    return new_arr
