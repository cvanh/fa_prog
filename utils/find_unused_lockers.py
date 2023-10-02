from utils.csv import read_csv 

def find_unused_lockers(size = 12):
    """finds the missing intergers whithin an array

    Args: 
        arr (array): the array where the missing intergers should be found
        size: (int): the biggest interger that should exist 
    """
    csv = read_csv() 

    # get the id's of lockers that are in use and convert that to an array
    # used_lockers = (csv.loc[:, "index"]).to_numpy()
    used_lockers = list(csv.index.values)
    
    used_lockers.sort()

    unused = []

    for item in range(size + 1) :
        if item not in used_lockers:
            unused.append(item)
    return unused


# print(len(find_unused_lockers([11],12)))
# print(len(find_unused_lockers([11,1,12],12)))
# print(len(find_unused_lockers([1,3,5,7,9,11],12)))
# print(len(find_unused_lockers([2,4,6,8,10,12],12)))