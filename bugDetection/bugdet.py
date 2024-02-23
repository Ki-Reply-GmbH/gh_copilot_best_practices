def merge_sorted_lists(list1, list2):
    # Initialize the merged list
    merged_list = []
    i, j = 0, 0

    # Loop through both lists to merge them
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    # Append the remaining elements of list1 (if any)
    while i < len(list1):
        merged_list.append(list1[i])
        i += 1

    # Append the remaining elements of list2 (if any)
    while j < len(list2):
        merged_list.append(list2[j])
        j += 1

    return merged_list

# Example usage
list1 = [1, 3,3, 5]
list2 = [2,3,4, 6, 8]
print(merge_sorted_lists(list1, list2))
