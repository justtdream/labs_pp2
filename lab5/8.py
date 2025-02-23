import re
with open(r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab5\row.txt', 'r') as file:
    match_text = file.read()

matches = re.split(r'(?=[A-Z])', match_text)
print(matches)