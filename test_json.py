# Import the json module
import json
from datetime import datetime
import pytz

time = "2024-01-01T00:33:18Z"
est = pytz.timezone("US/Eastern")

dt = datetime.fromisoformat(time)
loc_time = dt.astimezone(est)

date = loc_time.strftime("%m/%d/%Y, %H:%M:%S")

print(dt)
print(loc_time)
print(date)