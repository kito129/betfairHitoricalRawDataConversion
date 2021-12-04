# TODO

## IMPORTANT
### PATH
- [ ] set a variable where I can change all times the rawData path, cause isn't always the same -- rawData = "M:\05_BF_DATA\DATA" (string)
- [ ] the same with output folder, please use a variable where I can past everytime the correct output folder (as a string) --- exportOutput rawData = "M:\05_BF_DATA\EXPORT\LAST" (string)
- [ ] create a "exportOutput" folder with date and time in the path so if I run more than one time at day it doesn't override the output Data
- [ ] I want to add OTHER sport, so if a market is under /ADVANCED/OTHER or /BASIC/OTHER  just set the sport to OTHER and not add any additional info form excel
### CONSISTENCY
- [ ] uniform time, when you have to do with data or time please convert always in UTC millisecond timestamp (marketInfo.openDate, in marketUpdate.timeStamp and marketUpdate.openDate, and in odds timestamp too  )
- [ ] uniform soccer and football name, use always SOCCER terms
- [ ] fix venue and countyCode where is present ( venue only for HORSE)
- [ ] at the end of the process please empty all temp folder (rawInput)
### RUNNER DB
- [ ] for runner DB just save: id, name and sport (not all metadata of the odds)
- [ ] in runner DB when add runner please set the sport to, (ex. {"id": 28602170, "name": "Hyde Park Barracks", "sport":"HORSE"}, {"id": 39258079, "name": "Inter Milan", "sport":"SOCCER"}, {"id": 56598184, "name": "Novak Djokovic", "sport":"TENNIS"})
- [ ] for runner DB files please save with time too (date and time), cause if run the script 2 times a day it will be replaced
### FIX
- [ ] when check last market update to save the market info, if STATUS == "REMOVED" just skip the market
- [ ] in marketUpdate remove "complete" proprieties, I don't need that
- [x] change all NaN to null (NaN is not a valid JSON)
- [ ] it doesn't remove some TENNIS market with marketName contains "/" inside (ex. "Bara/Gorgodze v Piter/Sherif" is still present in output)
- [ ] the code already use by code to divide the sport (checkTennis and other functions) remove that and set sport based on where the market is placed in path (the code set HORSE for correct score market because have 16 runners, but is SOCCER )
- [ ] when calculate max and min prematch, if prematch not contain odds set to null
- [ ] please check the calculation, it appears a volume in the prematch when the metadata say that there aren't prematch
### LOG
- [ ] log the time elapsed for every sub task
- [ ] log info about how much market are generate, divided by sport and type (BASIC / ADVANCED)
 
 
- [ ] change the props name to this ones
```json
{
  "marketType": "ADVANCED",
  "marketInfo": {},
  "marketRunners": [],
  "marketUpdates": [],
  "marketOdds": [
    {
      "runnerId": 305969,
      "odd": []
    }
  ]
}
       
```

