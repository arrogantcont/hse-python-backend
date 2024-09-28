from math import factorial as math_factorial

def factorial(n: int) -> int:
    return math_factorial(n)

def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _  in range(n):
        a, b = b, a + b
    return a

def mean(numbers: list) -> int:
    return sum(numbers) / len(numbers)
