from functools import reduce
import operator

def multiply_list(numbers):
    return reduce(operator.mul, numbers, 1)

# Example
numbers = [2, 3, 4, 5]
result = multiply_list(numbers)
print("Product of all numbers:", result)


'''
reduce() — это встроенная функция из модуля functools, 
которая применяет функцию к элементам списка поочередно, сводя список к одному значению.

operator.mul — это встроенная функция из модуля operator, которая выполняет умножение (x * y).
Она эквивалентна lambda x, y: x * y, но работает быстрее, так как это встроенная операция.

'''