# FordPass data logger

This repo is a fork of the FordPass HomeAssistante integration. The intent is to significantly overhaul it to run as a standalone script and do some data logging for your vehicle.

At this time, the script is functional with the following sets of data pulled from Ford's APIs:

* vehicle_status
* vehicle_capability

**The current recommended minimum polling interval is <ins>15 minutes</ins>. Any shorter is liable to have your account locked out.**

Documentation on some of the data points provided from the API is available under [autonomicData.md](autonomicData.md)
