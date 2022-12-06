import math

def argmax_of_list(array):

    max_num=-1
    argmaxes = []

    for index, entry in enumerate(array):
        if entry > max_num:
            argmaxes = []
            argmaxes.append(index)
            max_num = entry
        elif entry == max_num:
            argmaxes.append(index)

    return argmaxes

def argmin_of_list(array):

    min_num = math.inf
    argmins = []

    for index, entry in enumerate(array):
        if entry < min_num:
            argmins = []
            argmins.append(index)
            min_num = entry
        elif entry == min_num:
            argmins.append(index)

    return argmins

def get_arg(array, value):
    # Assumes only one entry with value value in array

    for i, entry in enumerate(array):
        if entry == value:
            return i