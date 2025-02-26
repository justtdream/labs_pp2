def is_palindrome(s):
    s = s.lower().replace(" ", "")  
    return s == "".join(reversed(s)) 

# Example
print(is_palindrome("madam"))         # true
print(is_palindrome("racecar"))       # true
print(is_palindrome("hello"))         # false

