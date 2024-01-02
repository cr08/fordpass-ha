# Logic Brainstorming

This document is detailing my random thought process regarding the logic for some functions of this project. This will likely change as things develop

## Smart Refresh

Currently in a default state the `save_log.py` script just polls the Autonomic/Ford API and saves the resulting JSON to a new file. This doesn't always produce new data from the vehicle. This polling mode relies entirely on the vehicle (or a manual refresh from the FordPass app) sending updates when it deems necessary. This is limited to the following scenarios:

* Change to ignition ON
* (unverified) A few minutes after ignition ON
* Change to ignition OFF
* EVSE connection

A separate refresh command is available to force the vehicle to send new data. However in cases where the vehicle is powered off and not plugged in to a working EVSE, this causes the vehicle to wake up and draw extra power from the 12V battery until the update completes and it falls back asleep again. Constant, blind refreshes can cause the 12V battery to rapidly drain.

Some logic and scenarios I have in mind for when to do a forced refresh are as follows. For intervals above the 15m interval we have set, we'll do a simple time delta check from the last refresh and if the delta is >/= to the chosen interval, we'll run the refresh and update the last timestamp. Under normal polling, we should also check the JSON for an updated refresh timestamp and update our local timestamp from that in case of a refresh from an external source like the FordPass app.

* Ingition ON state - Refresh interval 15m
  * In this state, it is assumed the vehicle is powered on and running and 12V power is being actively supplied. We can do a regular refresh with hopefully no consequence
* Ingition OFF, EVSE CONNECTED state - Refresh interval ~1h
  * In this state, the vehicle is off and parked but an EVSE is connected. It is assumed if the car wakes up, the EVSE will be responsible for supplying 12V power via the onboard charger so we SHOULD be safe. However not much should change in this period, especially if the vehicle is on a scheduled charge profile and waiting to begin charging.
    * Further thinking about this one: We can monitor the charging status. If SCHEDULED, we can refresh every 1h. Under IN_PROGRESS, increase this to 15m which as of this writing is the fastest we can reliably refresh without risking running into Ford's banhammer. Once under COMPLETED we can return to a 1h interval.
* Ignition OFF, EVSE DISCONNECTED state - Refresh interval ~6h
  * This is the most crucial scenario. The vehicle is off and not plugged in, relying solely on the 12V battery. We also do not expect any significant changes during this period. 6h seems to be a decent interval but this may be adjusted in the future

## Database Storage

While a time-based DB like InfluxDB may be more optimal for this, I will be completely frank in that while researching it, it completely broke my brain. Being more familiar with relational databases, I will be going down this route and choosing Postgres as the DB server of choice.

Each sensor and data point will have its own table with columns for the updateTime, correlationId, and value entries from the JSON. Exceptions may be for the door and window statuses. I need to verify if there's any situations where the individual windows/doors may update without all of them updating.

Example table layout:

| updateTime         | correlationID | Value |
| ------------------ | ------------- | ----- |
| 20240102-16:58:00Z | 12345         | 100.0 |
| 20240102-17:00:00Z | 12346         | 98.0  |
