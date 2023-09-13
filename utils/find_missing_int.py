def find_missing_int(arr, size):
    """
    finds the missing intergers whithin an array

    Args: 
        arr (array): the array where the missing intergers should be found
        size: (int): the biggest interger that should exist 
    """
    missing = []

    for item in range(size):
        if item not in arr:
            missing.append(item)
    return missing

