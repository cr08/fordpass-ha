from datetime import datetime
import json
import os

from fordpass_new import Vehicle
from config import fordpass_username, fordpass_password, fordpass_vin, fordpass_region, veh_model, veh_year

cwd = os.path.dirname(os.path.abspath(__file__))
logs = os.path.join(cwd,"logs")

logs_exist = os.path.exists(logs)
if not logs_exist:
    os.makedirs(logs)
    print("\"logs\" subdirectory does not exist. Creating...")

VIC_YEAR = veh_year
VIC_MODEL = veh_model

veh = Vehicle()
vehicle_status = veh.status()
vehicle_capability = veh.vehicle_cap()

current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
if VIC_YEAR != "":
    VIC_YEAR = VIC_YEAR.replace(" ", "_") + "-"
if VIC_MODEL != "":
    VIC_MODEL = VIC_MODEL.replace(" ", "_")
else:
    VIC_MODEL = "my"

status_fileName = os.path.join(logs, f"chargelog_{VIC_YEAR}{VIC_MODEL}_{current_datetime}.json")
status_fileName = os.path.join(logs, f"status_{VIC_YEAR}{VIC_MODEL}_{current_datetime}.json")

if vehicle_capability != None:
        vehicleData = [vehicle_status, vehicle_capability]
else:
    # if VERBOSE:
    #     print("Unable to get vehicle capability, saving vehicle status")
    vehicleData = vehicle_status

# Write the redacted JSON data to the file

try:
    with open(status_fileName, 'w', encoding="utf-8") as file:
        try:
            json.dump(vehicleData, file, indent=4)
        except (IOError, OSError):
            print("Error writing to vehicleData JSON file")
except (FileNotFoundError, PermissionError, OSError):
    print("Error opening vehicleData JSON file")
