## Table of parameters supplied by Autonomic API

Units are specifically noted for clarity. By default everything is reported from the API in metric.

| JSON key                                                                      | 1st Gen Ford plug-in vehicles (C-Max Energi, Fusion Energi, etc.)            |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `metrics.customMetrics.aui:signal:xxx:custom:trip-sum-length`               | Total trip distance `(km)`                                                 |
| `metrics.customMetrics.aui:signal:xxx:custom-vehicle-trip-fuel-consumption` | Fuel (gas, diesel, etc.) quantity used during trip `(litres)`                   |
| `metrics.ambientTemp`                                                       | Ambient/Outside Temp `(Celsius)`                                           |
| `metrics.engineCoolantTemp`                                                 | Engine/ICE coolant temp `(Celsius)`                                        |
| `metrics.engineSpeed`                                                       | TBD                                                                          |
| `metrics.xevBatteryTimeToFullCharge`                                        | Estimated amount of time to complete HVB charging `(minutes)`              |
| `metrics.fuelLevel`                                                         | Fuel (gas, diesel, etc.) level `(%)`                                       |
| `metrics.fuelRange`                                                         | Hybrid/ICE vehicle range `(km)`                                            |
| `metrics.outsideTemperature`                                                | Ambient/Outside Temp `(Celsius)`                                           |
| `metrics.xevBatteryRange`                                                   | EV range `(km)`                                                |
| `metrics.xevBatteryStateOfCharge`                                           | EV HVB user displayed SOC `(%)`                                    |
| `metrics.torqueAtTransmission`                                              | Reported transmission torque output(?) `(newton meters/nm)`                 |
| `metrics.tripFuelEconomy`                                                   | Combined Hybrid/EV fuel economy of trip `(litres/100 km)`[<sup>1</sup>](#sub_1) |
| `metrics.tripXevBatteryRangeRegenerated`                                    | Trip Regen distance `(km)`                                                 |
| `metrics.tripXevBatteryChargeRegenerated`                                   | Trip Brake Score/Coach `(%)`                                               |
| `metrics.XevBatteryDistanceAccumulated`                                     | Estimated EV range added at last charge session `(km)`             |

<a name="sub_1"><sup>1</sup></a> For early model years (2013-2016?) the MPGe fuel economy display option was availabe in the vehicle cluster/IPC. This MPGe/MPG setting effects the data reported by this API. The API does not indicate which unit is being reported so it will need to be manually noted however you intend to use this data.