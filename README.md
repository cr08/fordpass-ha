# FordPass data logger

This repo is a fork of the FordPass HomeAssistant integration. The intent is to significantly overhaul it to run as a standalone script and do some data logging for your vehicle.

At this time, the script is functional with the following sets of data pulled from Ford's APIs:

* vehicle_status
* vehicle_capability
* charge_logs

### :warning: This is a WIP development repo. Use at your own risk. It may break at any time! :warning:

###### Instructions:

1. Fill out your credentials/info in config.py
2. Run `save_logs.py`
   1. eg: `python3 save_logs.py`
3. In the current state, it will pull and write a JSON file including the vehicle status/metrics and capabilities to the `./logs/` subfolder. Optionally charge logs will be written to a separate JSON if available (The Ford C-Max Energi does not have these sadly. This may also apply to the Fusion Energi)

❗**The current recommended minimum polling interval is <ins>15 minutes</ins>. Any shorter is liable to have your account locked out.** ❗

Documentation on some of the data points provided from the API is available under [autonomicData.md](autonomicData.md)
