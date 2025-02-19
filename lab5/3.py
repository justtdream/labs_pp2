import re
with open(r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab5\row.txt') as file:
    txt = file.read()
x = re.findall(r"\b[a-z]+_[a-z]+\b", txt)
print(x)