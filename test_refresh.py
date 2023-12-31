from datetime import datetime
import json
import os

from fordpass_new import Vehicle
from config import fordpass_vin, veh_model, veh_year, log_location

cwd = os.path.dirname(os.path.abspath(__file__))
if log_location:
    logs = log_location
else:
    logs = os.path.join(cwd,"logs")

# Check if designated log directory exists and create it if necessary.
try:
    os.makedirs(logs, exist_ok = True)
    print("Directory " + logs + " created successfully")
except OSError as error:
    print("Directory " + logs + " can not be created")

VIC_YEAR = veh_year
VIC_MODEL = veh_model

veh = Vehicle()

request_update = veh.request_update(fordpass_vin)

if request_update == "False":
    print("Vehicle update failed. Try later.")
else:
    with open("test.json", 'w', encoding="utf-8") as file:
        json.dump(request_update, file, indent=4)