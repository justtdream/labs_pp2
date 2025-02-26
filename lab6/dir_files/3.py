import os

path = r'C:\Users\WIN11\Desktop\study at uni\calc\calc2\Variant 0.pdf'
print("Our path", path)

print("Does our path exists?", os.path.exists(path))

if os.path.exists(path):
    if os.path.isfile(path):
        print("File's name:", os.path.basename(path))
        print("Path to the file:", os.path.dirname(path))
    else: print("Path to the directory:", os.path.dirname(path))