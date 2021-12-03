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
happens this error, please check and fix it (note: if batl, batb, tr or other value is not present in raw just leave it NaN), nut mantaine the strucure of JSON

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

NOTE: use as much as possible try and catch so if happens some problems with some market, just skip that and continue with others, to not interrupt the code (i want to start that and leave to process during night, so it will be soo annoying if I have to control all the time the execution  ) , and save in a list called marketError.json the market id and the path of all market that have some error inside
