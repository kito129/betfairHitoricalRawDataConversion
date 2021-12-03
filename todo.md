# TODO
* please use a varible where i can change all times the path to my folder in other HD where i have all raw file (as a string), cause itsn't always the same -- rawData
* the same with output folder, please use a variable where i can past everitime the correct output folder (as a string) --- exportOutput
* uniform soccer and football name, use always SOCCER terms
* uniform time, when you have to do with data or time please convert always in UTC millisecond timestamp
* as i said yesterday please fix venue and county code where is present ( venue only for HORSE)
* log info about how much market are generate, divided by sport an type (BASIC / ADVANCED)
* in runner DB when add runner please set the sport to, (ex. {"id": 28602170, "name": "Hyde Park Barracks", "sport":"HORSE"}, {"id": 39258079, "name": "Inter Milan", "sport":"SOCCER"}, {"id": 56598184, "name": "Novak Djokovic", "sport":"TENNIS"})
* when check last market update to save the market info, if STATUS == "REMOVED" just skip the market
* at the end of the process please empty all temp folder (rawInput)

# ERROR
happens this error, please check and fix it (note: if batl, batb, tr or other value is not present in raw just leave it null), nut mantaine the strucure of JSON


Traceback (most recent call last):
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\routine.py", line 19, in <module>
    main()
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\routine.py", line 15, in main
    process_all_json(json_paths)
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\process.py", line 56, in process_all_json
    for market in pool.imap(process_json, json_paths):
  File "C:\Python310\lib\multiprocessing\pool.py", line 870, in next
    raise value
KeyError: "['batl'] not in index"
