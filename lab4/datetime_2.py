from datetime import datetime, timedelta
now = datetime.now()
yesturday = datetime.now() + timedelta(days = -1)  
tomorrow = datetime.now() + timedelta(days = 1)


print (yesturday.date())
print (now.date())
print(tomorrow.date())
