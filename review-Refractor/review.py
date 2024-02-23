#TODO: Refactor it to make it more efficient and readable

def check_prime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def sum_of_evens_and_primes(l):
    sum_of_evens = 0
    sum_at_prime_indices = 0
    for i in range(len(l)):
        if l[i] % 2 == 0:
            sum_of_evens = sum_of_evens + l[i]
        if check_prime(i):
            sum_at_prime_indices = sum_at_prime_indices + l[i]
    print("Sum of even numbers: ", sum_of_evens)
    print("Sum of numbers at prime indices: ", sum_at_prime_indices)

# Example list
l = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

sum_of_evens_and_primes(l)
