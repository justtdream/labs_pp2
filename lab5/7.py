"""
camel case firstName 
snake case first_name
"""

import re
with open(r'C:\Users\WIN11\Desktop\study at uni\pp2\labs\lab5\row.txt', 'r') as file:
    match_text = file.read()

matches = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), match_text)
print(matches)