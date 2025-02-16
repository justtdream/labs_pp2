def counter(n):
    current = 0
    while current <= n:
        yield current
        current+=1
    
n = int(input("Enter number: "))

gen = counter(n)
for num in gen:
    print (num)
