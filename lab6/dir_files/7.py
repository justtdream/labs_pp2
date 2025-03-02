import os
file_path = r"C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab6\dir_files\text.txt"
copy_path = r"C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab6\dir_files\text_copy.txt"

with open(file_path, 'r') as source_file:
    content_to_copy = source_file.read()

with open(copy_path, 'w') as destination_file:
    destination_file.write(content_to_copy)