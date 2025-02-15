from datetime import datetime

def date_difference_in_seconds(date1, date2):
    format_str = "%Y-%m-%d %H:%M:%S"  
    d1 = datetime.strptime(date1, format_str)
    d2 = datetime.strptime(date2, format_str)
    
    difference = abs((d2 - d1).total_seconds())  
    return int(difference)

#Example 
date1 = "2024-02-15 12:00:00"
date2 = "2024-02-14 10:30:00"

result = date_difference_in_seconds(date1, date2)
print(f"Разница между датами в секундах: {result}")
