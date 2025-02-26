def all_elements_true(t):
    return all(t)  

# Example
print(all_elements_true((True, True, True)))   # True
print(all_elements_true((True, False, True)))  # False
print(all_elements_true((1, 2, 3)))            # True 
print(all_elements_true((1, 0, 3)))            # False 
print(all_elements_true(("", "Hello")))        # False 