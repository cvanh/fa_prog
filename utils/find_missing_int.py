def find_missing_int(arr, size):
    print("arr",arr)
    print("size",size)
    """finds the missing intergers whithin an array

    Args: 
        arr (array): the array where the missing intergers should be found
        size: (int): the biggest interger that should exist 
    """
    missing = []

    for item in range(size):
        if item not in arr:
            missing.append(item)
    return missing


print(len(find_missing_int([9,5,2],12)))
print(len(find_missing_int([9,3,2],12)))
print(len(find_missing_int([1,2],12)))
print(len(find_missing_int([2],12)))