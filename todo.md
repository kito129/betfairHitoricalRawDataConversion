# TODO
* please use a variable where I can change all times the path to my folder in other HD where i have all raw file (as a string), cause itsn't always the same -- rawData
* the same with output folder, please use a variable where I can past everytime the correct output folder (as a string) --- exportOutput
* uniform soccer and football name, use always SOCCER terms
* uniform time, when you have to do with data or time please convert always in UTC millisecond timestamp (marketInfo.openDate, in marketUpdate.timeStamp and marketUpdate.openDate, and in odds timestamp too  )
* as i said yesterday please fix venue and county code where is present ( venue only for HORSE)
* log info about how much market are generate, divided by sport and type (BASIC / ADVANCED)
* in runner DB when add runner please set the sport to, (ex. {"id": 28602170, "name": "Hyde Park Barracks", "sport":"HORSE"}, {"id": 39258079, "name": "Inter Milan", "sport":"SOCCER"}, {"id": 56598184, "name": "Novak Djokovic", "sport":"TENNIS"})
* when check last market update to save the market info, if STATUS == "REMOVED" just skip the market
* at the end of the process please empty all temp folder (rawInput)
* for runner DB files please save with time too, cause if run the script 2 times a day it will be replaced
* for runner DB just save: id, name and sport (not all metadata of the odds)
* in marketUpdate remove "complete" proprieties, i don't need that
* change all NaN to null please
* I want to add OTHER sport, so if a market is under /ADVANCED/OTHER or /BASIC/OTHER  just set the sport to OTHER and not add any additional info form excel 
* log the time elapsed for every task
* the code already use by code to divide the sport (checkTennis and other functions) remove that and set sport based on where the market is placed in path (the code set HORSE for correct score market beacusa have 16 runners, but is SOCCER )

* change the props name to this ones
```json
{
  "type": "ADVANCED",
  "marketInfo": {},
  "marketRunners": [....],
  "marketUpdates": [....],
  "marketOdds": [
    {
      "runnerId": 305969,
      "odd": [.....]
    }
  ]
}
       
```

# ERROR
* 1 - happens this error, please check and fix it (note: if batl, batb, tr or other value is not present in raw just leave it NaN), nut mantaine the strucure of JSON
  ```
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
    ```
  
* 2 - a different output but i think the same error
 ```
 JSON Files ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1691/65682   3% 0:39:422021-12-03 15:44:49.5372021-12-03 15:44:49.538 |  | ERROR   ERROR    |  | dataframedataframe::get_prices_dataframeget_prices_dataframe::166166 -  - A PRICE error occurred2021-12-03 15:44:49.584A PRICE error occurred
 | 
JSON Files ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1691/65682   3% 0:39:422021-12-03 15:44:49.643ERROR   2021-12-03 15:44:49.6352021-12-03 15:44:49.628 |  |  |  | ERROR   dataframe2021-12-03 15:44:49.770ERROR    |  | : | dataframeERROR   dataframeERROR   get_prices
:create_main_dataframe:166:166get_prices_dataframe: - :create_main_dataframe166:181 - 181 -  - A PRICE error occurred - A PRICE error occurredError creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670191\1.168155134.json


Error creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670193\1.167962705.jsonA PRICE error occurred2021-12-03 15:44:49.796

2021-12-03 15:44:49.797 |  | 2021-12-03 15:44:49.797ERROR    | ERROR   ERROR    |  |  | dataframedataframedataframe:::create_main_dataframecreate_main_dataframecreate_main_dataframe::181: - 181181Error creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670193\1.167962711.json -  -
Error creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670197\1.168155104.jsonError creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670193\1.167962710.json

2021-12-03 15:44:49.809 | ERROR    | dataframe:get_prices_dataframe:166 - A PRICE error occurred
2021-12-03 15:44:49.810 | ERROR    | dataframe:create_main_dataframe:181 - Error creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670197\1.168155109.json
JSON Files ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1691/65682   3% 0:39:422021-12-03 15:44:49.9292021-12-03 15:44:49.929 |  | ERROR   ERROR    |  | dataframedataframe::get_prices_dataframeget_prices_dataframe::166166 -  - A PRICE error occurredA PRICE error occurred

2021-12-03 15:44:49.9302021-12-03 15:44:49.930 |  | ERROR   ERROR    |  | dataframedataframe::create_main_dataframecreate_main_dataframe::181181 -  - Error creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670198\1.168155179.jsonError creating dataframe from path M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\rawInput\ADVANCED\SOCCER\2020\Feb\1\29670199\1.168155204.json

JSON Files ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1786/65682   3% 0:38:38
multiprocessing.pool.RemoteTraceback:
"""
Traceback (most recent call last):
  File "C:\Python310\lib\multiprocessing\pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\process.py", line 28, in process_json
    frame = create_main_dataframe(path, status)
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\dataframe.py", line 182, in create_main_dataframe
    raise e
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\dataframe.py", line 177, in create_main_dataframe
    'odds': get_prices_dataframe(path, status),
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\dataframe.py", line 167, in get_prices_dataframe
    raise e
  File "M:\03_PROJECT\04_BF\rawDataConversion\betfair-conversion\dataframe.py", line 164, in get_prices_dataframe
    prices_df_long = prices_df_long[columns]
  File "C:\Users\marco\AppData\Roaming\Python\Python310\site-packages\pandas\core\frame.py", line 3464, in __getitem__
    indexer = self.loc._get_listlike_indexer(key, axis=1)[1]
  File "C:\Users\marco\AppData\Roaming\Python\Python310\site-packages\pandas\core\indexing.py", line 1314, in _get_listlike_indexer
    self._validate_read_indexer(keyarr, indexer, axis)
  File "C:\Users\marco\AppData\Roaming\Python\Python310\site-packages\pandas\core\indexing.py", line 1377, in _validate_read_indexer
    raise KeyError(f"{not_found} not in index")
KeyError: "['batl'] not in index"
"""

The above exception was the direct cause of the following exception:

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

  ```
NOTE: use as much as possible try and catch so if happens some problems with some market, just skip that and continue with others, to not interrupt the code (i want to start that and leave to process during night, so it will be soo annoying if I have to control all the time the execution  ) , and save in a list called marketError.json the market id and the path of all market that have some error inside
