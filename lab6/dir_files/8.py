import os 

path = r"C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab6\dir_files\deleteit.txt"

if os.access(path, os.F_OK):
    os.remove(path)