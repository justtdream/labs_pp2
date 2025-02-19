import re
with open(r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab5\row.txt') as file:
    txt = file.read() 
x = re.findall('[A-Z][a-z]+', txt)
print(x)
