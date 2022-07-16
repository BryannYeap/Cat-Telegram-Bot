import math

# Creates a 2D-list from the given flat 1D-list, where the inner list has a number of columns specified by the num_of_cols param
def two_dimension_listify(num_of_cols, flat_list):
    two_dimension_list = []
    row = []

    for element in flat_list:
        row.append(element)

        if len(row) == num_of_cols:
            two_dimension_list.append(row)
            row = []

    return two_dimension_list

def binary_search(element, sorted_list):
    if (len(sorted_list) == 1):
        return 0
    
    start = 0
    end = len(sorted_list) - 1

    while (end > start):
        mid = math.floor(((end - start) / 2)) + start

        if (sorted_list[mid] >= element):
            end = mid
        elif (sorted_list[mid] < element):
            start = mid + 1

    if (sorted_list[start] == element):
        return start
    else:
        return -1; 
