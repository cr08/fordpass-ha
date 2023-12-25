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
vehicle_status = veh.status()
charge_logs = veh.charge_log()

vehicle_capability = veh.vehicle_cap()
# Deleting status key from vehicle profile/capability JSON data.
# This has a timestamp that changes at every poll and interferes with future change checks.
del vehicle_capability["userVehicles"]["status"]

current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
if VIC_YEAR != "":
    VIC_YEAR = VIC_YEAR.replace(" ", "_") + "-"
if VIC_MODEL != "":
    VIC_MODEL = VIC_MODEL.replace(" ", "_")
else:
    VIC_MODEL = "my"

clog_fileName = os.path.join(logs, f"chargelog_{VIC_YEAR}{VIC_MODEL}_{current_datetime}.json")
status_fileName = os.path.join(logs, f"status_{VIC_YEAR}{VIC_MODEL}_{current_datetime}.json")
vehiclecap_filename = os.path.join(logs, f"{fordpass_vin}_vehinfo.json")

# Check for Vehicle Capability result and write to JSON if available
if vehicle_capability != None:
    # Check if an existing vehicle profile/capability log exists. If not, write our results from the API.
    # If it exists, update the file with the new data. This file should not change regularly.
    if os.path.isfile(vehiclecap_filename) and os.access(vehiclecap_filename, os.R_OK):
        with open(vehiclecap_filename, "r") as f:
            cap_file_data = json.load(f)
        if vehicle_capability == cap_file_data:
            print("Vehicle profile/capability data has not changed. Skipping...")
        else:
            print("Vehicle profile/capability data has changed. Writing new data to " + vehiclecap_filename)
    else:
        print("Vehicle profile/capability log has not been generated. Writing new data to " + vehiclecap_filename)
        try:
            with open(vehiclecap_filename, 'w', encoding="utf-8") as file:
                try:
                    json.dump(vehicle_capability, file, indent=4)
                except (IOError, OSError):
                    print("Error writing to vehicle_capability JSON file")
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening vehicle_capability JSON file")
else:
    print("Unable to get vehicle capability")

# Write Vehicle Status/Metrics to JSON file
try:
    with open(status_fileName, 'w', encoding="utf-8") as file:
        try:
            json.dump(vehicle_status, file, indent=4)
        except (IOError, OSError):
            print("Error writing to vehicleData JSON file")
except (FileNotFoundError, PermissionError, OSError):
    print("Error opening vehicleData JSON file")


# Check if Charge Logs pulled from API have data. If empty or the 'energyTransferLogs' key is empty as seen on some vehicles, skip writing a file
if not 'energyTransferLogs' in charge_logs or len(charge_logs['energyTransferLogs']) == 0:
    print("No charge logs. Skipping...")
else:
    try:
        with open(clog_fileName, 'w', encoding="utf-8") as file:
            try:
                json.dump(charge_logs, file, indent=4)
            except (IOError, OSError):
                print("Error writing to charge_log JSON file")
    except (FileNotFoundError, PermissionError, OSError):
        print("Error opening charge_log JSON file")
