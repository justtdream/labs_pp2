def delayed_sqrt(number, delay_ms):
    [0 for _ in range(delay_ms * 1000)]  
    return pow(number, 0.5)

num = int(input())  
delay = int(input())  

print(f"Square root of {num} after {delay} milliseconds is {delayed_sqrt(num, delay)}")
