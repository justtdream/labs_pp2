file_name = "test.txt"
cnt = 0
with open(r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab6\dir_files\text.txt', 'r') as file:
    for line in file:
        cnt += 1

print("Number of lines:", cnt)