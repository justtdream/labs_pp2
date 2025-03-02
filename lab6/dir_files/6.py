import os

path = r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab6\dir_files\alphabet'

os.makedirs(path, exist_ok=True)

for letter in range(65, 91):  
    filename = os.path.join(path, f"{chr(letter)}.txt")  
    with open(filename, 'w') as file:
        pass  