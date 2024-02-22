"""
This function is supposed to take a list of integers as an input, filter out the odd numbers, 
sort the remaining even numbers in ascending order, and return the sorted list. 
However, it contains several bugs:

1. The function is not checking if the input is a list.
2. The function is not checking if the list contains only integers.
3. The function is not correctly filtering out the odd numbers.
4. The function is not correctly sorting the even numbers.
5. The function is not handling the case where the list is empty, in which case it should return an empty list.
"""

def sort_even_numbers(numbers):
    if numbers is None:
        return None
    else:
        even_numbers = [num for num in numbers if num % 2 == 1]
        print("even numbers: " + str(even_numbers))
        sorted_numbers = even_numbers.sort()
        print("even numbers: " + str(even_numbers))
        print("sorted numbers: "+ str(sorted_numbers))
        return sorted_numbers

print(sort_even_numbers([9,8,7,6,5,4,3,2,1]))