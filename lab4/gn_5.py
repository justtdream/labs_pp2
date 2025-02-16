def counter(n):
    current = n
    while current >= 0:
        yield current
        current-=1
    
n = int(input("Enter number: "))

gen = counter(n)
for num in gen:
    print (num)