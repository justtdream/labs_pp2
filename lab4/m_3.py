import math
n = int(input("Input number of sides: "))
s = int(input("Input the length of a side: "))  
if n == 4:
    area = s**2
else:
    area = (n * s**2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", area)
