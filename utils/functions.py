from typing import List, Union
from math import factorial as factorial_n

def factorial(n: int) -> int: 
    return factorial_n(n)

def fibonacci(n: int) -> int: 
    if n <= 1: 
        return 1
    else: 
        return fibonacci(n-1) + fibonacci(n-2)

def mean(array: List[Union[int, float]]) -> Union[int, float]:
    return sum(array)/len(array)