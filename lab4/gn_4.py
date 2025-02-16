def square(a, b):
    for i in range (a, b+1):
        yield i ** 2

a = int(input("Enter start value: "))
b = int(input("Enter end value: "))

gen = square(a, b)
for num in gen:
    print(num)