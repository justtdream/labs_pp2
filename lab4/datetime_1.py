from datetime import datetime, timedelta
now = datetime.now()
tomorrow = datetime.now() + timedelta(days = 1)  
nextday = datetime.now() + timedelta(days = 2)
nextnextday = datetime.now() + timedelta(days = 3)
nextnextnextday = datetime.now() + timedelta(days = 4)
nextnextnextnextday = datetime.now() +timedelta(days = 5)

print (now.date())
print(tomorrow.date())
print(nextday.date())
print(nextnextday.date())
print(nextnextnextday.date())
print(nextnextnextnextday.date())