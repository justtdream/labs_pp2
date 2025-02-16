def counter(n):
    current = 0
    while current <= n:
        if current%3 == 0 and current%4 == 0:
            yield current 
        current+=1
    
n = int(input("Enter number: "))

gen = counter(n)
for num in gen:
    print (num)
