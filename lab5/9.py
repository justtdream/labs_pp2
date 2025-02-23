import re
with open(r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab5\row.txt', 'r') as file:
    match_text = file.read()

def insertspaces(text):
    return re.sub(r'(?<!\s)(?=[A-Z])', ' ', text).strip()

result = insertspaces(match_text)
print(result)