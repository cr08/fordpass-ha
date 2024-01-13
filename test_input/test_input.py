import json
import os
import sys
# import requests
import glob
import psycopg2
# from datetime import datetime

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from config import pgsql_host, pgsql_db, pgsql_user, pgsql_password

cwd = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(cwd, "logs")
diffdir = os.path.join(cwd, "diff")

logbasename = "status_*.json"

filepattern = os.path.join(logdir, logbasename)
logfiles = glob.glob(filepattern)

logfiles = sorted(logfiles)

conn = psycopg2.connect(database=pgsql_db, user=pgsql_user, password=pgsql_password, host=pgsql_host)
cur = conn.cursor()

def insert_metrics_main(funjs, sensor, text=False):
    table = "metrics." + sensor
    
    oemCorrelationId = funjs["metrics"][sensor]["oemCorrelationId"]
    updateTime = funjs["metrics"][sensor]["updateTime"]
    value = funjs["metrics"][sensor]["value"]
    
    if text:
        sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value) VALUES({oemCorrelationId}, \'{updateTime}\', \'{value}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
    else:
        sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value) VALUES({oemCorrelationId}, \'{updateTime}\', {value}) ON CONFLICT (oemCorrelationId) DO NOTHING;"
    cur.execute(sql)  
    conn.commit()
    
    # delete key from JSON data
    del funjs["metrics"][sensor]
    
def insert_metrics_tripkeys(funjs, sensor):
    table = "metrics." + sensor
    # idname = sensor + ".oemCorrelationId"
    
    oemCorrelationId = funjs["metrics"][sensor]["oemCorrelationId"]
    updateTime = funjs["metrics"][sensor]["updateTime"]
    value = funjs["metrics"][sensor]["value"]
    tripProgress = funjs["metrics"][sensor]["tripProgress"]
    
    sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value, tripProgress) VALUES({oemCorrelationId}, \'{updateTime}\', {value}, \'{tripProgress}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
    cur.execute(sql)  
    conn.commit()
    
    # delete key from JSON data
    del funjs["metrics"][sensor]
    
def insert_metrics_doorStatus(funjs, sensor):
    table = "metrics." + sensor
    # idname = sensor + ".oemCorrelationId"
    
    oemCorrelationId = funjs["oemCorrelationId"]
    updateTime = funjs["updateTime"]
    value = funjs["value"]
    
    sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value) VALUES({oemCorrelationId}, \'{updateTime}\', \'{value}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
    cur.execute(sql)  
    conn.commit()
    
    # delete key from JSON data
    del oemCorrelationId
    del updateTime
    del value
    del funjs["vehicleDoor"]
    del funjs["vehicleOccupantRole"]
    
def insert_metrics_windowStatus(funjs, sensor):
    table = "metrics." + sensor
    # idname = sensor + ".oemCorrelationId"
    
    oemCorrelationId = funjs["oemCorrelationId"]
    updateTime = funjs["updateTime"]
    lowerBound = funjs["value"]["doubleRange"]["lowerBound"]
    upperBound = funjs["value"]["doubleRange"]["upperBound"]
    
    sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, lowerbound, upperbound) VALUES({oemCorrelationId}, \'{updateTime}\', \'{lowerBound}\', \'{upperBound}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
    cur.execute(sql)  
    conn.commit()
    
    # delete key from JSON data
    del oemCorrelationId
    del updateTime
    del lowerBound
    del upperBound
    del funjs["vehicleWindow"]
    del funjs["vehicleOccupantRole"]
    del funjs["vehicleSide"]
    
for filename in logfiles:
    print("FILE: " + filename)
    with open(filename, "r") as file:
        js = json.load(file)

        # Removing vehicle cap/profile data from existing JSON files from old combined data.
        for i in list(js):
            if "userVehicles" in i:
                print("Vehicle Cap #1 found . Deleting.")
                del js[1]
                js = js[0]
    
        # Looping through all possible metrics data points we need to store
        for i in list(js["metrics"]):
            # Insert JSON data for basic sensors with oemCorrelationId, updateTime, and value columns
            if "acceleratorPedalPosition" in i:
                insert_metrics_main(js, "acceleratorPedalPosition")
            elif "ambientTemp" in i:
                insert_metrics_main(js, "ambientTemp")
            elif "engineCoolantTemp" in i:
                insert_metrics_main(js, "engineCoolantTemp")
            elif "engineSpeed" in i:
                insert_metrics_main(js, "engineSpeed")
            elif "xevBatteryTimeToFullCharge" in i:
                insert_metrics_main(js, "xevBatteryTimeToFullCharge")
            elif "fuelLevel" in i:
                insert_metrics_main(js, "fuelLevel")
            elif "fuelRange" in i:
                insert_metrics_main(js, "fuelRange")
            elif "hoodStatus" in i:
                insert_metrics_main(js, "hoodStatus", True)
            elif "hybridVehicleModeStatus" in i:
                insert_metrics_main(js, "hybridVehicleModeStatus", True)
            elif "ignitionStatus" in i:
                insert_metrics_main(js, "ignitionStatus", True)
            elif "outsideTemperature" in i:
                insert_metrics_main(js, "outsideTemperature")
            elif "wheelTorqueStatus" in i:
                insert_metrics_main(js, "wheelTorqueStatus", True)
            elif "remoteStartCountdownTimer" in i:
                insert_metrics_main(js, "remoteStartCountdownTimer")
            elif "oilLifeRemaining" in i:
                insert_metrics_main(js, "oilLifeRemaining")
            elif "odometer" in i:
                insert_metrics_main(js, "odometer")
            elif "speed" in i:
                insert_metrics_main(js, "speed")
            elif "vehicleLifeCycleMode" in i:
                insert_metrics_main(js, "vehicleLifeCycleMode", True)
            elif "xevPlugChargerStatus" in i:
                insert_metrics_main(js, "xevPlugChargerStatus", True)
            elif "xevBatteryRange" in i:
                insert_metrics_main(js, "xevBatteryRange")
            elif "xevBatteryStateOfCharge" in i:
                insert_metrics_main(js, "xevBatteryStateOfCharge")
            elif "xevBatteryPerformanceStatus" in i:
                insert_metrics_main(js, "xevBatteryPerformanceStatus", True)
            elif "torqueAtTransmission" in i:
                insert_metrics_main(js, "torqueAtTransmission")
            elif "xevBatteryChargeDisplayStatus" in i:
                insert_metrics_main(js, "xevBatteryChargeDisplayStatus", True)
            # Insert JSON data for trip specific sensors including the tripProgress column
            elif "tripFuelEconomy" in i:
                insert_metrics_tripkeys(js, "tripFuelEconomy")
            elif "tripXevBatteryRangeRegenerated" in i:
                insert_metrics_tripkeys(js, "tripXevBatteryRangeRegenerated")
            elif "tripXevBatteryChargeRegenerated" in i:
                insert_metrics_tripkeys(js, "tripXevBatteryChargeRegenerated")
            elif "tripXevBatteryDistanceAccumulated" in i:
                insert_metrics_tripkeys(js, "tripXevBatteryDistanceAccumulated")
            elif "compassDirection" in i:
                # compassDirection
                sensor = "compassDirection"
                table = "metrics." + sensor
                # idname = sensor + ".oemCorrelationId"
                
                oemCorrelationId = js["metrics"][sensor]["oemCorrelationId"]
                updateTime = js["metrics"][sensor]["updateTime"]
                value = js["metrics"][sensor]["value"]
                gpsModuleTimestamp = js["metrics"][sensor]["gpsModuleTimestamp"]
                
                sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value, gpsModuleTimestamp) VALUES({oemCorrelationId}, \'{updateTime}\', \'{value}\', \'{gpsModuleTimestamp}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
                cur.execute(sql)  
                conn.commit()
                
                # delete key from JSON data
                del oemCorrelationId
                del updateTime
                del value
                del gpsModuleTimestamp
            elif "heading" in i:
                # heading
                sensor = "heading"
                table = "metrics." + sensor
                # idname = sensor + ".oemCorrelationId"
                
                oemCorrelationId = js["metrics"][sensor]["oemCorrelationId"]
                updateTime = js["metrics"][sensor]["updateTime"]
                heading = js["metrics"][sensor]["value"]["heading"]
                uncertainty = js["metrics"][sensor]["value"]["uncertainty"]
                detectionType = js["metrics"][sensor]["value"]["detectionType"]
                gpsModuleTimestamp = js["metrics"][sensor]["gpsModuleTimestamp"]
                
                sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, heading, uncertainty, detectionType, gpsModuleTimestamp) VALUES({oemCorrelationId}, \'{updateTime}\', {heading}, {uncertainty}, \'{detectionType}\', \'{gpsModuleTimestamp}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
                cur.execute(sql)  
                conn.commit()
                
                # delete key from JSON data
                del oemCorrelationId
                del updateTime
                del heading
                del uncertainty
                del detectionType
                del gpsModuleTimestamp
            elif "parkingBrakeStatus" in i:
                # compassDirection
                sensor = "parkingBrakeStatus"
                table = "metrics." + sensor
                # idname = sensor + ".oemCorrelationId"
                
                oemCorrelationId = js["metrics"][sensor]["oemCorrelationId"]
                updateTime = js["metrics"][sensor]["updateTime"]
                value = js["metrics"][sensor]["value"]
                parkingBrakeType = js["metrics"][sensor]["parkingBrakeType"]
                
                sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value, parkingBrakeType) VALUES({oemCorrelationId}, \'{updateTime}\', \'{value}\', \'{parkingBrakeType}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
                cur.execute(sql)  
                conn.commit()
                
                # delete key from JSON data
                del oemCorrelationId
                del updateTime
                del value
                del parkingBrakeType
            elif "position" in i:
                # position
                sensor = "position"
                table = "metrics." + sensor
                # idname = sensor + ".oemCorrelationId"
                
                oemCorrelationId = js["metrics"][sensor]["oemCorrelationId"]
                updateTime = js["metrics"][sensor]["updateTime"]
                lat = js["metrics"][sensor]["value"]["location"]["lat"]
                lon = js["metrics"][sensor]["value"]["location"]["lon"]
                alt = js["metrics"][sensor]["value"]["location"]["alt"]
                gpsDimension = js["metrics"][sensor]["value"]["gpsDimension"]
                gpsCoordinateMethod = js["metrics"][sensor]["value"]["gpsCoordinateMethod"]
                pdop = js["metrics"][sensor]["value"]["pdop"]
                hdop = js["metrics"][sensor]["value"]["hdop"]
                vdop = js["metrics"][sensor]["value"]["vdop"]
                gdop = js["metrics"][sensor]["value"]["gdop"]
                gpsModuleTimestamp = js["metrics"][sensor]["gpsModuleTimestamp"]
                
                sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, lat, lon, alt, gpsDimension, gpsCoordinateMethod, pdop, hdop, vdop, gdop, gpsModuleTimestamp) VALUES({oemCorrelationId}, \'{updateTime}\', {lat}, {lon}, {alt}, \'{gpsDimension}\', \'{gpsCoordinateMethod}\', {pdop}, {hdop}, {vdop}, {gdop}, \'{gpsModuleTimestamp}\') ON CONFLICT (oemCorrelationId) DO NOTHING;"
                cur.execute(sql)  
                conn.commit()
                
                # delete key from JSON data
                del oemCorrelationId
                del updateTime
                del lat
                del lon
                del alt
                del gpsDimension
                del gpsCoordinateMethod
                del pdop
                del hdop
                del vdop
                del gdop
                del gpsModuleTimestamp
            elif "doorStatus" in i:
                # doorStatus - Looping through doorStatus object, parsing out individual door status items        
                for item in js["metrics"]["doorStatus"]:
                    # Front Left door/Driver
                    if item["vehicleDoor"] == "UNSPECIFIED_FRONT" and item["vehicleSide"] == "DRIVER":
                        insert_metrics_doorStatus(item, "doorstatus_frontleft")
                    # Front Right door/Passenger
                    elif item["vehicleDoor"] == "UNSPECIFIED_FRONT" and item["vehicleSide"] == "PASSENGER":
                        insert_metrics_doorStatus(item, "doorstatus_frontright")
                    # Rear Right door/Passenger
                    elif item["vehicleDoor"] == "REAR_RIGHT":
                        insert_metrics_doorStatus(item, "doorstatus_rearright")
                    # Rear Left door/Passenger
                    elif item["vehicleDoor"] == "REAR_LEFT":
                        insert_metrics_doorStatus(item, "doorstatus_rearleft")
                    # Tailgate
                    elif item["vehicleDoor"] == "TAILGATE":
                        insert_metrics_doorStatus(item, "doorstatus_tailgate")
                    # Ignoring any other entries in the doorStatus item
            elif "windowStatus" in i:
                # windowStatus - Looping through windowStatus object, parsing out individual window status items
                for item in js["metrics"]["windowStatus"]:
                    # Front Left door/Driver
                    if item["vehicleWindow"] == "UNSPECIFIED_FRONT" and item["vehicleSide"] == "DRIVER":
                        insert_metrics_windowStatus(item, "windowstatus_frontleft")
                    # Front Right door/Passenger
                    elif item["vehicleWindow"] == "UNSPECIFIED_FRONT" and item["vehicleSide"] == "PASSENGER":
                        insert_metrics_windowStatus(item, "windowstatus_frontright")
                    # Rear Right door/Passenger
                    elif item["vehicleWindow"] == "UNSPECIFIED_REAR" and item["vehicleSide"] == "PASSENGER":
                        insert_metrics_windowStatus(item, "windowstatus_rearright")
                    # Rear Left door/Passenger
                    elif item["vehicleWindow"] == "UNSPECIFIED_REAR" and item["vehicleSide"] == "DRIVER":
                        insert_metrics_windowStatus(item, "windowstatus_rearleft")
                    
        # trip-sum-length
        sensor = "aui:signal:745a2a40-3327-4943-bdf8-f71d9b389d8b:custom:trip-sum-length"
        table = "metrics.\"trip-sum-length\""
        # idname = "trip-sum-length.oemCorrelationId"
        
        oemCorrelationId = js["metrics"]["customMetrics"][sensor]["oemCorrelationId"]
        updateTime = js["metrics"]["customMetrics"][sensor]["updateTime"]
        value = js["metrics"]["customMetrics"][sensor]["value"]
        
        sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value) VALUES({oemCorrelationId}, \'{updateTime}\', {value}) ON CONFLICT (oemCorrelationId) DO NOTHING;"
        cur.execute(sql)  
        conn.commit()
        
        # delete key from JSON data
        del oemCorrelationId
        del updateTime
        del value
        
        # vehicle-trip-fuel-consumption
        sensor = "aui:signal:745a2a40-3327-4943-bdf8-f71d9b389d8b:custom:vehicle-trip-fuel-consumption"
        table = "metrics.\"vehicle-trip-fuel-consumption\""
        # idname = "vehicle-trip-fuel-consumption.oemCorrelationId"
        
        oemCorrelationId = js["metrics"]["customMetrics"][sensor]["oemCorrelationId"]
        updateTime = js["metrics"]["customMetrics"][sensor]["updateTime"]
        value = js["metrics"]["customMetrics"][sensor]["value"]
        
        sql = f"INSERT INTO {table}(oemCorrelationId, updateTime, value) VALUES({oemCorrelationId}, \'{updateTime}\', {value}) ON CONFLICT (oemCorrelationId) DO NOTHING;"
        cur.execute(sql)  
        conn.commit()
        
        # delete key from JSON data
        del oemCorrelationId
        del updateTime
        del value
    
        # Looping through all possible event data points we need to store
        for i in list(js["events"]):
            if "configurationResetEvent" in i:
                table = "events.configurationResetEvent"
                updateTime = js["events"]["configurationResetEvent"]["updateTime"]
                for cond in list(js["events"]["configurationResetEvent"]["conditions"]):
                    conditions = cond
                ftcp_version = js["events"]["configurationResetEvent"]["oemData"]["ftcp_version"]["stringValue"]
                sql = f"INSERT INTO {table}(updateTime, conditions, ftcp_version) VALUES(\'{updateTime}\', \'{conditions}\', \'{ftcp_version}\') ON CONFLICT (updateTime) DO NOTHING;"
                cur.execute(sql)  
                conn.commit()
            # elif "torqueSourceDeliveryEvent" in i:
            #     print("DERP")
            #     # insert_metrics_main(js, "ambientTemp")
            elif "remoteStartEvent" in i:
                table = "events.remoteStartEvent"
                updateTime = js["events"]["remoteStartEvent"]["updateTime"]
                for cond in list(js["events"]["remoteStartEvent"]["conditions"]):
                    conditions = cond
                ftcp_version = js["events"]["remoteStartEvent"]["oemData"]["ftcp_version"]["stringValue"]
                sql = f"INSERT INTO {table}(updateTime, conditions, ftcp_version) VALUES(\'{updateTime}\', \'{conditions}\', \'{ftcp_version}\') ON CONFLICT (updateTime) DO NOTHING;"
                cur.execute(sql)  
                conn.commit()
            
        # Looping through all possible state data points we need to store
        # for i in list(js["states"]):
        #     if "deviceWakeup" in i:
        #         # insert_metrics_main(js, "acceleratorPedalPosition")
        #     elif "deviceConnectivity" in i:
        #         # insert_metrics_main(js, "ambientTemp")
        #     elif "unlockCommand" in i:
        #         # derp
        #     elif "remoteStartCommand" in i:
        #         # derp
        #     elif "configurationUpdate" in i:
        #         # derp
        #     elif "statusRefreshCommand" in i:
        #         # derp
            
    # with open(filename + ".json", "w") as f:
    #     json.dump(js, f, indent=4)
        

conn.commit()
cur.close()
conn.close()