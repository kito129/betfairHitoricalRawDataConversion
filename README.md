# RAW BETFAIR TO MY JSON

These are the required project specifications.
All material is based on the code contained in /code

I ask that you follow the project specifications strictly, but feel free to make the best changes necessary to make the code robust, reliable, and performant as it will be the basis of a very large project I plan to develop.

The code for the moment logs little data but I would like that for each task done are shown on screen the metrics of each step
For example:
Total files to process
Total corrected files
Total runners generated
Eventual errors at run time or raw files not conforming to the specifications



The following docs index:

Specification

* [Other Repo](#other-repo)
* [Raw Data definition](#raw-data-definition)

* Downloading RAW data from Betfair
*  Extracting the archives and dividing by sport and data type
*  Creation of the temporal data frame
*  Splitting of data and first JSON
*  Data conversion into specification
*  Correction of temporal bugs
*  Save metadata quotas and runners
*  Runner list creation
*  Saving and split in folders of final files


----------------------------
## Other repo

Some repo and links related to the project

* [Betfair Historical Data website](https://historicdata.betfair.com/#/help)
* [Betfair Official Developer Program](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Developer+Support)
* [historic-data-workbook](https://github.com/betfair/historic-data-workbook)
* [historicdata](https://github.com/betfair/historicdata)
* [API-NG-Excel-Toolkit](https://github.com/betfair/API-NG-Excel-Toolkit)
* [AwesomeBetfair](https://github.com/betfair-down-under/AwesomeBetfair)
* [flumine](https://github.com/marcoselva/flumine)
* [betfair](https://github.com/liampauling/betfair)
* [betfairdata](https://github.com/liampauling/betfairdata)
* [betfair](https://github.com/liampauling/betfair)
* [betfair](https://betfair-datascientists.github.io/)

## Raw Data definition

* [Betfair Docs](https://github.com/marcoselva/rawDataConversion/blob/main/documentation/Betfair-Historical-Data-Feed-Specification.pdf)

The database on which we will operate will be purchased from Betfair exchange and will include all the matches on the platform, with information about:
* The market event information
* The market updates (event OPEN, SUSPENDED, CLOSED, the status of inPlay and betDelay..).
* The runner's information (the competitors of the event) 
* The odds (price, volume and available prices to bet).

Additional data information ( such as final result, bookmaker odds and some stats) that will be add over a 
* [Soccer Additional Data](https://github.com/marcoselva/rawDataConversion/tree/main/excel/SOCCER)
* [Tennis Additional Data](https://github.com/marcoselva/rawDataConversion/tree/main/excel/TENNIS)


This is a sample of market Djokovic v Medvedev of 12/09/2021

ADVANCED[`1.187528277.bz2.json`](https://github.com/marcoselva/rawDataConversion/blob/main/sample/input/ADVANCED/1.187528277.bz2.json)

BASIC[`1.187528277.bz2.json`](https://github.com/marcoselva/rawDataConversion/blob/main/sample/input/BASIC/1.187528277.bz2.json)


As you can see this is a list of Market change in the time (pt is published time), and the main propose is to convert this time data in
* A single version of market info (event, name, time, open date and all info about the market) -> from now on we will call it <b> MarketInfo</b>
* A single version of market runners, all info about runners of the markets (id, name, position...) -> from now on we will call it <b> MarketRunners</b>
* The odd information during the time about all runners in the market (time of update, price, volume and available prices...) -> from now on we will call it <b> MarketPrices</b>
* The update of the market during the time (open, suspended market, in play, event start, event closed...) -> from now on we will call it <b> MarketUpdates</b>

As you can see there are two types of data:
* BASIC
* ADVANCED

Both contain the same information, but 
* ADVANCED has updates every second and complex odds data (time, odds, traded volume, available to bet)  
* BASIC has updates every minute and the only odds information is only timestamp and last traded prices (odds)

### The raw data folder are
* [Raw data ADVANCED](https://github.com/marcoselva/rawDataConversion/tree/main/rawData/ADVANCED)
* [Raw data BASIC](https://github.com/marcoselva/rawDataConversion/tree/main/rawData/BASIC)

each folder contains subfolder
* /TENNIS
* /SOCCER
* /HORSE RACING


## Market Specification

### Market Sport
| # 	| sport 	|
|---	|---	|
| 1 	| HORSE RACING 	|
| 2 	| SOCCER 	|
| 3 	| TENNIS 	|

### Market Type

The market type list you should use

| # 	| marketType 	| eventName 	| sport 	| note 	| nOfRunners 	|
|---	|---	|---	|---	|---	|---	|
| 1 	| WIN 	| Winner 	| HORSE RACING 	| winner of the race 	| typical #2 ore more runners, the name of runners, ex: End Zone, State Secretary, Daniel Deronda...  	|
| 2 	| MATCH_ODDS 	| Match Odds 	| SOCCER 	| winner of the match 	| #3: 2 name of the team and The Draw, ex: Inter, Juventus, The Draw	|
| 3 	| HALF_TIME 	| Half Time 	| SOCCER 	| winner of the half-time 	| #3: 2 name of the team and The Draw, ex: Inter, Juventus, The Draw	|
| 4 	| BOTH_TEAMS_TO_SCORE 	| Both teams to Score? 	| SOCCER 	| both teams score at least one goal 	| #2: Yes, No 	|
| 5 	| OVER_UNDER 05 	| Over/Under 0.5 Goals 	| SOCCER 	|  number of the goals in the match 	| #2: Under 0.5 Goals, Over 0.5 Goals 	|
| 6 	| OVER_UNDER 15 	| Over/Under 1.5 Goals 	| SOCCER 	|  number of the goals in the match 	| #2: Under 1.5 Goals, Over 1.5 Goals 	|
| 7 	| OVER_UNDER 25 	| Over/Under 2.5 Goals 	| SOCCER 	|  number of the goals in the match 	| #2: Under 2.5 Goals, Over 2.5 Goals 	|
| 8 	| OVER_UNDER 35 	| Over/Under 3.5 Goals 	| SOCCER 	|  number of the goals in the match 	| #2: Under 3.5 Goals, Over 3.5 Goals 	|
| 9 	| OVER_UNDER 45 	| Over/Under 4.5 Goals 	| SOCCER 	|  number of the goals in the match 	| #2: Under 4.5 Goals, Over 4.5 Goals 	|
| 10 	| OVER_UNDER 55 	| Over/Under 5.5 Goals 	| SOCCER 	|  number of the goals in the match 	| #2: Under 5.5 Goals, Over 5.5 Goals 	|
| 11 	| FIRST_HALF_GOALS_05 	| First Half Goals 0.5 	| SOCCER 	|  number of the goals in the half-time 	| #2: Under 0.5 Goals, Over 0.5 Goals 	|
| 12 	| FIRST_HALF_GOALS_15 	| First Half Goals 1.5 	| SOCCER 	|  number of the goals in the half-time 	| #2: Under 1.5 Goals, Over 1.5 Goals 	|
| 13 	| FIRST_HALF_GOALS_25 	| First Half Goals 2.5 	| SOCCER 	|  number of the goals in the half-time 	| #2: Under 2.5 Goals, Over 2.5 Goals 	|
| 14 	| FIRST_HALF_GOALS_35 	| First Half Goals 3.5 	| SOCCER 	|  number of the goals in the half-time 	| #2: Under 3.5 Goals, Over 3.5 Goals 	|
| 15 	| CORRECT_SCORE 	| Correct Score 	| SOCCER 	| correct result of the match 	| typical #16 +#3 always present: 0-0, 0-1, 0-2, 0-3, 1-0, 2-0, 3-0, 1-2, 2-1, 3-1, 1-3, 3-2, 2-3,1-1, 2-2, 3-3, Any Other Home Win, Any Other Away Win, Any Other Draw 	|
| 16 	| MATCH_ODDS 	| Match Odds 	| TENNIS 	| winner of the match 	| #2: the player Name ex. Novak Djokovic, Daniil Medvedev 	|

# TASK TO DO

## 1- Download data and Extract principal ZIP

The first process to do is to download the data form [Betfair](https://historicdata.betfair.com/#/home)
This process includes purchase and authentication task, so I don't want to automate that process.

I will provide you a sample of data to working about.
Then I will use for my self the code over all data to create my personal db.

The code should be run once a day, as the data is released after 5 days from the end of the event.
So this code will need to be run once a day to add the newly downloaded markets to the DB.

Every day I will place the data in the /rawData (separated in SPORT) folder and start the code.


I'll put all the .bz2 archive in this folders

`rawData/BASIC/SOCCER/`
`rawData/BASIC/TENNIS/`
`rawData/BASIC/HORSE RACING/`

`rawData/ADVANCED/SOCCER/`
`rawData/ADVANCED/TENNIS/`
`rawData/ADVANCED/HORSE RACING/`


## 2- Extract all market

The current code start with placing the correct folder to analyze in the path (we fix to convert all path in the same time)
`code/routine.py` 

```bash
  python routine.py
```


```python

# the path were al files are extracted, you have to sperate file extracted by sport and by type of data
workPath = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/code/rawInput/'

# the path were i will place the file to be converted
data_ADVANCED_SOCCER = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/ADVANCED/SOCCER/'
data_ADVANCED_TENNIS = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/ADVANCED/TENNIS/'
data_ADVANCED_HORSE_RACING = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/ADVANCED/HORSE RACING/'

data_BASIC_SOCCER = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/BASIC/SOCCER/'
data_BASIC_TENNIS = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/BASIC/TENNIS/'
data_BASIC_HORSE_RACING = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/BASIC/HORSE RACING/'

# have to run for all above folder

# start the routine
main.main(data_BASIC_HORSE_RACING,workPath,'BASIC')

```

For the moment the code runs one folder at a time and I have to change the path, but in the new project it should do everything together and eventually divide the markets again by type (ADV / BASIC) and by sport

We hould extract the .bz2 archive in all sub folder and save as JSON

I created this code, that you have to fix and improve with sport differentiation and type too (BASIC / ADVANCED)

```python
# ##
#  --- IMPORT ---
# ##
import os
import bz2
import json


# loop on all folder in path and extract bz2 to JSON file
def extractJson(dataPath, extractPath):
    print("\nExtracting File...")
    countOK = 0
    for (dirpath, dirnames, files) in os.walk(dataPath):
        for fileName in files:
            # filter out decompressed files
            if fileName.endswith('.json'):
                continue

            # save file as .json
            filepath = os.path.join(dirpath, fileName)
            newFilepath = extractPath + fileName + '.json'
           

            # save JSON file
            with open(newFilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
                for data in iter(lambda: file.read(), b''):
                    new_file.write(data)
            file.close()
            countOK = countOK +1

    # print recap
    print("Files Extracted: " + str(countOK))
    print('\nEnd of extraction..\n')
```

At the end of this process we could have a folder ( at the moment i didn't implement the sport division)

`code/rawInput/BASIC/SOCCER/`
`code/rawInput/BASIC/TENNIS/`
`code/rawInput/BASIC/HORSE RACING/`

`code/rawInput/ADVANCED/SOCCER/`
`code/rawInput/ADVANCED/TENNIS/`
`code/rawInput/ADVANCED/HORSE RACING/`

contains all raw archive data converted to correct JSON format
 
## 3- Convert to JSONv1

Now start the real conversion task.

### Panda dataframe and line separation
`code/dataframe.py` is were the code made this dataframe creation and division about type lines and different info

I convert this `1.1.187528277.json` to a panda dataframe in order to separate all lines and save the pt (publish time in milliseconds UTC)

There will be 2 different types of line:

#### MARKET CHANGES
This one have "mc" props, inside that "marketDefinition" props and not "rc" props

```json
{
  "op": "mcm",
  "clk": "4210380045",
  "pt": 1631334824468,
  "mc": [
    {
      "id": "1.187528277",
      "marketDefinition": {
        "bspMarket": false,
        "turnInPlayEnabled": true,
        "persistenceEnabled": true,
        "marketBaseRate": 5.0,
        "eventId": 30891863,
        "eventTypeId": "2",
        "numberOfWinners": 1,
        "bettingType": "ODDS",
        "marketType": "MATCH_ODDS",
        "marketTime": "2021-09-12T20:00:00.000Z",
        "suspendTime": "2021-09-12T20:00:00.000Z",
        "bspReconciled": false,
        "complete": true,
        "inPlay": false,
        "crossMatching": true,
        "runnersVoidable": false,
        "numberOfActiveRunners": 2,
        "betDelay": 0,
        "status": "OPEN",
        "runners": [
          {
            "status": "ACTIVE",
            "sortPriority": 1,
            "id": 2249229,
            "name": "Novak Djokovic"
          },
          {
            "status": "ACTIVE",
            "sortPriority": 2,
            "id": 19924831,
            "name": "Daniil Medvedev"
          }
        ],
        "regulators": [
          "MR_INT"
        ],
        "countryCode": "US",
        "discountAllowed": true,
        "timezone": "Europe/London",
        "openDate": "2021-09-12T20:00:00.000Z",
        "version": 4023449846,
        "name": "Match Odds",
        "eventName": "Djokovic v Medvedev"
      }
    }
  ]
}
  ```
#### ODDS UPDATE
This one have "mc" props, inside that ahve "rc" props and not "marketDefinition" props

```json
{
  "op": "mcm",
  "clk": "4211879304",
  "pt": 1631350227393,
  "mc": [
    {
      "id": "1.187528277",
      "rc": [
        {
          "batl": [
            [0,3.4,75.81 ]
          ],
          "ltp": 3.35,
          "tv": 3392.42,
          "id": 19924831
        },
        {
          "trd": [
            [1.42,11327.93]
          ],
          "batb": [
            [ 0,1.42, 38.05],
            [1,1.41,1604.61],
            [2,1.4,551.3]
          ],
          "batl": [
            [0,1.43,1790.57],
            [1,1.44,927.71],
            [2,1.45,1399.42]
          ],
          "ltp": 1.42,
          "tv": 16440.85,
          "id": 2249229
        }
      ]
    }
  ],
  .....
}
```

At the end of process of dataframe creation we could have this division

```python
mainObj = {
  'market': getMarketDataframe(path),
  'runners': getRunnerDataframe(path),
  'odds': getPricesDataframe(path, status)
}
```

This is an example of data contained

`mainObj['market']`

|    | publish_time               |      id |   eventId | marketType   | openDate                 | status    | eventName           | name       |   betDelay | inPlay   | complete   |   numberOfActiveRunners |    version |
|---:|:---------------------------|--------:|----------:|:-------------|:-------------------------|:----------|:--------------------|:-----------|-----------:|:---------|:-----------|------------------------:|-----------:|
|  0 | 2021-09-11 03:27:17.213000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T15:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023427524 |
|  1 | 2021-09-11 03:27:18.736000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T15:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023427524 |
|  2 | 2021-09-11 04:33:40.969000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T15:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023449846 |
|  3 | 2021-09-11 04:33:44.468000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic @ Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023449846 |
|  4 | 2021-09-11 05:58:50.202000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023467671 |
|  5 | 2021-09-11 05:58:59.435000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023468035 |
|  6 | 2021-09-12 20:01:53.477000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029685094 |
|  7 | 2021-09-12 20:01:55.685000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:15:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029685094 |
|  8 | 2021-09-12 20:11:58.503000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:15:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029701160 |
|  9 | 2021-09-12 20:12:01.419000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029701160 |
| 10 | 2021-09-12 20:17:12.479000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029712768 |
| 11 | 2021-09-12 20:17:13.160000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 12 | 2021-09-12 21:56:08.717000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 13 | 2021-09-12 21:57:00.519000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 14 | 2021-09-12 21:57:07.713000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 15 | 2021-09-12 21:57:12.713000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 16 | 2021-09-12 21:57:50.645000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 17 | 2021-09-12 21:58:01.693000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 18 | 2021-09-12 21:58:53.670000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 19 | 2021-09-12 21:58:54.651000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 20 | 2021-09-12 21:58:58.660000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 21 | 2021-09-12 21:59:21.643000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 22 | 2021-09-12 21:59:31.687000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 23 | 2021-09-12 22:00:39.674000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 24 | 2021-09-12 22:00:40.548000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 25 | 2021-09-12 22:00:47.590000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 26 | 2021-09-12 22:01:09.689000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 27 | 2021-09-12 22:01:44.644000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 28 | 2021-09-12 22:01:47.638000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 29 | 2021-09-12 22:01:57.697000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 30 | 2021-09-12 22:01:58.673000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 31 | 2021-09-12 22:02:02.592000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 32 | 2021-09-12 22:03:21.581000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 33 | 2021-09-12 22:03:28.483000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 34 | 2021-09-12 22:03:51.712000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 35 | 2021-09-12 22:05:00.717000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 36 | 2021-09-12 22:05:16.714000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 37 | 2021-09-12 22:07:11.468000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 38 | 2021-09-12 22:07:13.689000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 39 | 2021-09-12 22:14:31.644000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 40 | 2021-09-12 22:14:43.636000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 41 | 2021-09-12 22:14:48.656000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 42 | 2021-09-12 22:16:17.685000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 43 | 2021-09-12 22:16:35.670000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 44 | 2021-09-12 22:18:53.379000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 45 | 2021-09-12 22:19:01.566000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 46 | 2021-09-12 22:21:20.580000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 47 | 2021-09-12 22:22:31.688000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 48 | 2021-09-12 22:22:38.386000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 49 | 2021-09-12 22:22:58.533000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 50 | 2021-09-12 22:23:26.524000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 51 | 2021-09-12 22:23:43.668000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 52 | 2021-09-12 22:23:49.660000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 53 | 2021-09-12 22:24:04.643000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 54 | 2021-09-12 22:24:22.704000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 55 | 2021-09-12 22:24:30.608000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 56 | 2021-09-12 22:25:15.490000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 57 | 2021-09-12 22:27:33.716000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 58 | 2021-09-12 22:28:45.654000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 59 | 2021-09-12 22:29:03.661000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 60 | 2021-09-12 22:29:54.623000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 61 | 2021-09-12 22:30:19.544000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 62 | 2021-09-12 22:30:57.704000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 63 | 2021-09-12 22:31:47.665000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 64 | 2021-09-12 22:31:48.588000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 65 | 2021-09-12 22:31:50.658000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 66 | 2021-09-12 22:32:02.706000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 67 | 2021-09-12 22:32:59.558000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 68 | 2021-09-12 22:33:15.675000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 69 | 2021-09-12 22:33:26.482000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029883744 |
| 70 | 2021-09-12 22:36:23.103000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | CLOSED    | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       0 | 4029887210 |


For market update we should remove the identical update lines (line with no changes except "publish_time" and "version" value), and remove version value

this is my code to that (to imporve and fix=
```python
# remove similar line 
newUpdate = []
newUpdate.append(self.marketUpdates[0])
for index, elem in enumerate(self.marketUpdates):
    if(index>0):
        if(not(self.marketUpdates[index-1]['openDate'] == elem['openDate'] and
            self.marketUpdates[index-1]['status'] == elem['status'] and
            self.marketUpdates[index-1]['betDelay'] == elem['betDelay'] and
            self.marketUpdates[index-1]['inPlay'] == elem['inPlay'])):
                newUpdate.append(elem)

self.marketUpdates = newUpdate
```

So for this file we should have this 

`mainObj['market"]` // removed identical lines

|    | publish_time               |      id |   eventId | marketType   | openDate                 | status    | eventName           | name       |   betDelay | inPlay   | complete   |   numberOfActiveRunners |
|---:|:---------------------------|--------:|----------:|:-------------|:-------------------------|:----------|:--------------------|:-----------|-----------:|:---------|:-----------|------------------------:|
|  0 | 2021-09-11 03:27:17.213000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T15:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 |
|  3 | 2021-09-11 04:33:44.468000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic @ Medvedev | Match Odds |          0 | False    | True       |                       2 |
|  4 | 2021-09-11 05:58:50.202000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 |
|  5 | 2021-09-11 05:58:59.435000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 |
|  7 | 2021-09-12 20:01:55.685000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:15:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 |
|  9 | 2021-09-12 20:12:01.419000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 |
| 10 | 2021-09-12 20:17:12.479000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 |
| 11 | 2021-09-12 20:17:13.160000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 |
| 69 | 2021-09-12 22:33:26.482000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 |
| 70 | 2021-09-12 22:36:23.103000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | CLOSED    | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       0 |


`mainObj['runners"]`

|     | status   |       id | name            |   sortPriority |
|----:|:---------|---------:|:----------------|---------------:|
| 1 | LOSER    |  2249229 | Novak Djokovic  |              1 |
| 2 | WINNER   | 19924831 | Daniil Medvedev |              2 |


`mainObj['odds"]` // some lines are removed here to view


|       | publish_time               |   runner_id | runner_name     |   odds |          tv | trd                                   | batb                                    | batl                                                            |   sortPriority |
|------:|:---------------------------|------------:|:----------------|-------:|------------:|:--------------------------------------|:----------------------------------------|:----------------------------------------------------------------|---------------:|       
|  9818 | 2021-09-12 22:19:35.713000 |    19924831 | Daniil Medvedev |   1.01 | 6.68472e+06 | [[1.01, 9.17]]                        | [[0, 1.01, 142355.73]]                  | [[0, 1.02, 56460.02]]                                           |              2 |       
|  9828 | 2021-09-12 22:19:47.555000 |    19924831 | Daniil Medvedev |   1.01 | 6.69197e+06 | [[1.01, 2423.62]]                     | [[0, 1.01, 141183.56]]                  | nan                                                             |              2 |       
| 10029 | 2021-09-12 22:23:26.524000 |    19924831 | Daniil Medvedev |   1.01 | 6.86352e+06 | [[1.01, 60000.53], [1.02, 470821.02]] | [[0, 1.01, 32819.33], [1, 1.01, 0]]     | nan                                                             |              2 |       
| 10030 | 2021-09-12 22:23:27.658000 |    19924831 | Daniil Medvedev |   1.01 | 6.86352e+06 | nan                                   | [[0, 1.02, 156.73], [1, 1.01, 41358.3]] | [[1, 1.04, 19773.08]]                                           |              2 |       
| 10031 | 2021-09-12 22:23:28.644000 |    19924831 | Daniil Medvedev |   1.01 | 6.86352e+06 | nan                                   | [[1, 1.01, 49896.43]]                   | [[0, 1.03, 26970.37]]                                           |              2 |       
| 10032 | 2021-09-12 22:23:29.520000 |    19924831 | Daniil Medvedev |   1.01 | 6.86352e+06 | nan                                   | nan                                     | [[0, 1.03, 27213.09], [1, 1.04, 14758.89]]                      |              2 |       
| 10035 | 2021-09-12 22:23:32.670000 |    19924831 | Daniil Medvedev |   1.01 | 6.86423e+06 | [[1.01, 60000.77], [1.02, 471523.44]] | [[0, 1.01, 45859.5]]                    | [[0, 1.02, 51.46]]                                              |              2 |       
| 10036 | 2021-09-12 22:23:33.654000 |    19924831 | Daniil Medvedev |   1.01 | 6.86423e+06 | nan                                   | nan                                     | [[0, 1.02, 416.39]]                                             |              2 |       
| 10037 | 2021-09-12 22:23:34.168000 |    19924831 | Daniil Medvedev |   1.01 | 6.86423e+06 | nan                                   | [[0, 1.01, 45869.5]]                    | nan                                                             |              2 |       
| 10623 | 2021-09-12 22:33:25.556000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | [[1.01, 61163.32]]                    | nan                                     | [[0, 1.01, 23918.93], [1, 1.02, 4011.13], [2, 1.04, 46.22]]     |              2 |       
| 10624 | 2021-09-12 22:33:28.655000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | nan                                   | nan                                     | [[2, 1.04, 41.1]]                                               |              2 |       
| 10625 | 2021-09-12 22:33:30.956000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | nan                                   | nan                                     | [[2, 1.04, 3.81]]                                               |              2 |       
| 10626 | 2021-09-12 22:33:42.587000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | nan                                   | nan                                     | [[0, 1.02, 4011.13], [1, 1.04, 3.81], [2, 1.05, 3585.56]]       |              2 |       
| 10627 | 2021-09-12 22:33:44.085000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | nan                                   | nan                                     | [[1, 1.05, 3585.56], [2, 1.06, 4753.31]]                        |              2 |       
| 10628 | 2021-09-12 22:33:56.976000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | nan                                   | nan                                     | [[0, 1.15, 50.42], [1, 1.2, 79], [2, 1.3, 43.7]]                |              2 |       
| 10629 | 2021-09-12 22:34:13.765000 |    19924831 | Daniil Medvedev |   1.01 | 7.5221e+06  | nan                                   | nan                                     | [[0, 1.2, 59.42], [1, 1.3, 23.7], [2, 1.47, 20.07]]             |              2 |      
| 22124 | 2021-09-12 22:22:23.628000 |     2249229 | Novak Djokovic |    100 | 4.28571e+06 | [[100, 10]]                             | [[0, 100, 7.8], [1, 80, 42.69], [2, 60, 8.54]]    | [[0, 120, 2.05], [1, 200, 1.5], [2, 230, 2]]   |              1 |
| 22125 | 2021-09-12 22:22:24.668000 |     2249229 | Novak Djokovic |    100 | 4.28571e+06 | nan                                     | [[2, 65, 144]]                                    | [[1, 150, 2], [2, 200, 1.5]]                   |              1 |
| 22126 | 2021-09-12 22:22:25.651000 |     2249229 | Novak Djokovic |    100 | 4.28571e+06 | nan                                     | [[1, 80, 61.48]]                                  | nan                                            |              1 |
| 22127 | 2021-09-12 22:22:26.680000 |     2249229 | Novak Djokovic |    100 | 4.28571e+06 | nan                                     | [[0, 100, 3], [2, 70, 8.54]]                      | nan                                            |              1 |
| 22128 | 2021-09-12 22:22:27.665000 |     2249229 | Novak Djokovic |     95 | 4.28571e+06 | [[95, 4]]                               | [[0, 95, 5.23], [1, 85, 79.89], [2, 80, 61.48]]   | nan                                            |              1 |
| 22129 | 2021-09-12 22:22:28.645000 |     2249229 | Novak Djokovic |     95 | 4.28571e+06 | nan                                     | [[0, 85, 89.89], [1, 80, 61.48], [2, 70, 8.54]]   | [[2, 180, 2]]                                  |              1 |
| 22130 | 2021-09-12 22:22:29.681000 |     2249229 | Novak Djokovic |     95 | 4.28571e+06 | nan                                     | [[0, 85, 64.27], [1, 80, 42.69], [2, 65, 144]]    | nan                                            |              1 |
| 22163 | 2021-09-12 22:23:18.040000 |     2249229 | Novak Djokovic |     85 | 4.28596e+06 | [[85, 94.46], [90, 27.94]]              | [[0, 85, 11.57], [1, 60, 53.16], [2, 55, 13.23]]  | nan                                            |              1 |
| 22164 | 2021-09-12 22:23:19.224000 |     2249229 | Novak Djokovic |     85 | 4.28596e+06 | nan                                     | [[0, 60, 53.16], [1, 55, 13.23], [2, 50, 1.71]]   | nan                                            |              1 |
| 22165 | 2021-09-12 22:23:20.514000 |     2249229 | Novak Djokovic |    100 | 4.28596e+06 | [[100, 113.3]]                          | nan                                               | [[0, 100, 7.73]]                               |              1 |
| 22166 | 2021-09-12 22:23:22.633000 |     2249229 | Novak Djokovic |    100 | 4.28596e+06 | nan                                     | nan                                               | [[0, 85, 7.23], [1, 100, 7.73], [2, 200, 1.5]] |              1 |
| 22167 | 2021-09-12 22:23:23.617000 |     2249229 | Novak Djokovic |    100 | 4.28596e+06 | nan                                     | [[0, 55, 13.23], [1, 50, 1.71], [2, 48, 1.71]]    | [[2, 110, 10.63]]                              |              1 |


### Panda dataframe to python object

Now we have completed conversion from original raw file to panda dataframe

It's the moment to start to convert in python object

We pass this obj to convertToMyObject(dataframe, path, status) function tha is in `code/dfToObeject.py`

in this file i separate MarketInfo, MarketSelection, MarketUpdates, MarketPrices entities and i covert panda df to python obj

The class is defined in `code/object/markets.py` 
The constructor take the dataframe and create a python object based on last market update

I take into consideration the <b>last market changes update</b> for makert info and runners to be sure to get the complete and correct info (based on the fact that they are the info on which will be based the settlement of the market and then its closing)


### Match updates fix (correct openDate)
Now we start with match update fix

In practice there is an "error" on the data reported by betfair. The starting time reported in the market update (openDate) is almost never correct to the thousandth because that value (openDate) is set according to the official time of, but then the match starts at a different time (sometimes we talk about a few seconds or minutes, while in other cases the deviation can be much larger.

To correct this error

```python
    # fix start match error
    mainMarket.fixUpdates()
```

|    | publish_time               |      id |   eventId | marketType   | openDate                 | status    | eventName           | name       |   betDelay | inPlay   | complete   |   numberOfActiveRunners |    version |
|---:|:---------------------------|--------:|----------:|:-------------|:-------------------------|:----------|:--------------------|:-----------|-----------:|:---------|:-----------|------------------------:|-----------:|
|  0 | 2021-09-11 03:27:17.213000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T15:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023427524 |
|  3 | 2021-09-11 04:33:44.468000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic @ Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023449846 |
|  4 | 2021-09-11 05:58:50.202000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023467671 |
|  5 | 2021-09-11 05:58:59.435000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:00:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4023468035 |
|  7 | 2021-09-12 20:01:55.685000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:15:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029685094 |
|  9 | 2021-09-12 20:12:01.419000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029701160 |
| 10 | 2021-09-12 20:17:12.479000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          0 | False    | True       |                       2 | 4029712768 |
| 11 | 2021-09-12 20:17:13.160000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | OPEN      | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029713448 |
| 69 | 2021-09-12 22:33:26.482000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | SUSPENDED | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       2 | 4029883744 |
| 70 | 2021-09-12 22:36:23.103000 | 1.18753 |  30891863 | MATCH_ODDS   | 2021-09-12T20:08:00.000Z | CLOSED    | Djokovic v Medvedev | Match Odds |          3 | True     | True       |                       0 | 4029887210 |


like here as you can see betfair report for openDate = 2021-09-12T20:08:00.000Z, but the correct in play time is 2021-09-12 20:17:13.160000, and we can find it iterating over the marketUpdate array and stopping the search when these conditions are all true:

* status = 'OPEN'
* inPlay = True
* betDelay > 0

something like this 
```python
inPlayTime = 0
#find open time for market Update
for elem in self.marketUpdates:
    if elem['inPlay'] and elem['status'] == 'OPEN' and elem['betDelay'] >0 :
        inPlayTime = int(elem['timestamp'])
        break
``` 

### Removing some market
Now we can save the info about correct openDate and the betDelay time

There are some rule to remove / skip the market if betDelay are to high

* Tennis --> remove if (betdelay >3 and open date > 2019)
* Tennis --> remove if (betdelay >5 and open date < 2019)
* Football --> remove if betdelay > 7

And ONLY FOR TENNIS, we should remove match with "/" in event name (all doubles matches, that i don't want in my DB)
* Tennis --> remove if eventName contains "/" or " / "


### Improve runner info and odds information

Now the object is complete, it's the time to improve runners metadata based on odd information.

```python
    # update updates with odds for the status
    mainMarket.updateRunnersStats(status)
```

With this code we save this info about the runners

* runners['inPlayOdds']: the first odds (ltp values) after the market is inPlay (first runners odds after openDate time)
* runners['inPlayIndex']: the first odds (ltp values) after the market is inPlay (the index in odds array)
* runners['inPlayTime']: the first odds timestamp (ltp values) after the market is inPlay (the first timestamp for this runner after openDate )
* runners['closedOdds']: the last odds (ltp values) for the runner
* runners['avgPrematch']: the average odds before openDate
* runners['maxPrematch']: the max odds reached (ltp values) by the runner before the openDate time
* runners['minPrematch']: the min odds reached (ltp values) by the runner before the openDate time
* runners['maxInPlay']: the max odds reached (ltp values) by the runner after the openDate time
* runners['minInPlay']: the min odds reached (ltp values) by the runner after the openDate time
* runners['lengthOdds']: the total lenght of the odds array
* runners['lengthOddsPrematch']: the total lenght of the odds before the openDate
* runners['lengthOddsInPlay']: the total lenght of the odds from the openDate to the market CLOSE
### Volume  info for ADVANCED

if status == 'ADVANCED': 

* runners['tradedVolume']: the total traded volume on this runner (should be the last chronological "tv" volume)
* runners['preMatchVolume']: the total traded volume on this runner before the open date
* runners['inPlayVolume']: the total traded volume on this runner from the open date to the end CLOSE of the market


```python
 # update odds for status in updates
    def updateRunnersStats(self, status):

        inPlay = self.info['openDate']
        runners = self.runners
        odds = self.odds

        # find inplay for all runners
        for run in runners:

            sumPrematch = 0
            stepCounter = 0
            contPrematch = 0
            maxPrematch = -100
            minPrematch = 1001
            maxInPlay = -100
            minInPlay = 1001
            found = False

            # volume for runner
            preMatchVolume = 0

            # iterate over odds
            for odd in odds:
                if odd['runnerId'] == run['id']:
                    # find inPlay index
                    inPlayindex = int(self._find_inPlay_index(odd, inPlay))
                    if len(odd['odds']) > 0 and inPlayindex > -1:
                        for _odd in odd['odds']:
                            # avg runner prematch odd
                            if stepCounter < inPlayindex:
                                # check if max prematch
                                if _odd['ltp'] > maxPrematch:
                                    maxPrematch = _odd['ltp']
                                # check if min prematch
                                if _odd['ltp'] < minPrematch:
                                    minPrematch = _odd['ltp']
                                # increment prematch counter
                                sumPrematch = sumPrematch + _odd['ltp']
                                contPrematch = contPrematch + 1

                            elif stepCounter >= inPlayindex:
                                # im in INPLAY
                                # set the first inplay ltp as inPlayOdds
                                if not found:
                                    # volume for ADVANCED only (check volume)
                                    if status == 'ADVANCED':
                                        preMatchVolume = _odd['tv']
                                    # inPlay time and odds
                                    run['inPlayOdds'] = _odd['ltp']
                                    run['inPlayTime'] = _odd['timestamp']
                                    found = True
                                # check if max inplay
                                if _odd['ltp'] > maxInPlay:
                                    maxInPlay = _odd['ltp']
                                # check if min inplay
                                if _odd['ltp'] < minInPlay:
                                    minInPlay = _odd['ltp']
                            # increment step counter
                            stepCounter = stepCounter + 1
                        # avg odds prematch 
                        if contPrematch != 0:
                            run['avgPrematch'] = round(sumPrematch / contPrematch,2)
                        else:
                            run['avgPrematch'] = 0
                        # closed odds
                        run['closedOdds'] = odd['odds'][len(odd['odds']) - 1]['ltp']
                        # max and min prematch
                        run['maxPrematch'] = maxPrematch
                        run['minPrematch'] = minPrematch
                        # max and min inPlay
                        run['maxInPlay'] = maxInPlay
                        run['minInPlay'] = minInPlay
                        # odds metadata
                        run['inPlayIndex'] = inPlayindex
                        run['lengthOdds'] = stepCounter
                        run['lengthOddsPrematch'] = contPrematch
                        run['lengthOddsInPlay'] = stepCounter - contPrematch
                        # volume for ADVANCED
                        if status == 'ADVANCED':
                            run['tradedVolume'] = round(odd['odds'][len(odd['odds']) - 1]['tv'],2)
                            run['preMatchVolume'] = round(preMatchVolume,2)
                            run['inPlayVolume'] = round(run['tradedVolume'] - preMatchVolume,2)
                    # no odds for this runner
                    else:
                        run['inPlayOdds'] = 0
                        run['openOdds'] = 0
                        run['closedOdds'] = 0
                        run['maxPrematch'] = 0
                        run['minPrematch'] = 0
                        run['maxInPlay'] = 0
                        run['minInPlay'] = 0
                        # volume for ADVANCED
                        if status == 'ADVANCED':
                            run['tradedVolume'] = 0
                            run['preMatchVolume'] = 0
                            run['inPlayVolume'] = 0

    # update total market volume based on runner traded volume
    def updateVolume(self):

        for runnerVol in self.runners:
            self.info['volume']['total'] = round(self.info['volume']['total'] +  runnerVol['tradedVolume'],2)
            self.info['volume']['preMatch'] = round(self.info['volume']['preMatch'] +  runnerVol['preMatchVolume'],2)
            self.info['volume']['inPlay'] = round(self.info['volume']['inPlay'] +  runnerVol['inPlayVolume'],2)

    # find inPlay index for this runner
    def _find_inPlay_index(self, runnerOdds, inPlayTime):

        counter = 0
        minCounter = -1
        for value in runnerOdds['odds']:
            if value['timestamp'] - inPlayTime >= 0:
                minCounter = counter
                break
            counter = counter + 1
        return minCounter
```


After this pass we should save this info in file, with improved runner info that should looks likes: (odds part are ommised)

```json
{
  "info": {
    "id": "1.187528277",
    "eventId": 30891863,
    "eventName": "Match Odds",
    "marketType": "MATCH_ODDS",
    "openDate": 1631477833160,
    "name": "Djokovic v Medvedev",
    "numberOfActiveRunner": 2,
    "numberOfWinners": 1,
    "bspMarket": false,
    "turnInPlayEnabled": true,
    "persistenceEnabled": true,
    "timezone": "Europe/London",
    "countryCode": "US",
    "sport": "TENNIS",
    "venue": "",
    "volume": {
      "total": 11825068.38,
      "preMatch": 1852569.96,
      "inPlay": 9972498.42
    },
    "winner": {
      "id": 19924831,
      "name": "Daniil Medvedev",
      "status": "WINNER",
      "position": 2
    },
    "delay": 3
  },
  "runners": [
    {
      "id": 2249229,
      "name": "Novak Djokovic",
      "status": "LOSER",
      "position": 1,
      "inPlayOdds": 1.44,
      "inPlayTime": 1631477833160,
      "avgPrematch": 1.42,
      "closedOdds": 19.0,
      "maxPrematch": 1.44,
      "minPrematch": 1.38,
      "maxInPlay": 120.0,
      "minInPlay": 1.41,
      "inPlayIndex": 4532,
      "lengthOdds": 12014,
      "lengthOddsPrematch": 4532,
      "lengthOddsInPlay": 7482,
      "tradedVolume": 4302965.3,
      "preMatchVolume": 1578301.23,
      "inPlayVolume": 2724664.07
    },
    {
      "id": 19924831,
      "name": "Daniil Medvedev",
      "status": "WINNER",
      "position": 2,
      "inPlayOdds": 3.3,
      "inPlayTime": 1631477833160,
      "avgPrematch": 3.34,
      "closedOdds": 1.01,
      "maxPrematch": 3.55,
      "minPrematch": 3.25,
      "maxInPlay": 3.45,
      "minInPlay": 1.01,
      "inPlayIndex": 3013,
      "lengthOdds": 10613,
      "lengthOddsPrematch": 3013,
      "lengthOddsInPlay": 7600,
      "tradedVolume": 7522103.08,
      "preMatchVolume": 274268.73,
      "inPlayVolume": 7247834.35
    }
  ],
  "marketUpdates": [
    { 
      "timestamp":  1631330837213000000,
      "openDate":   1631458800000,
      "status": "OPEN",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631334824468000000,
      "openDate": 1631476800000,
      "status": "OPEN",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631339930202000000,
      "openDate": 1631476800000,
      "status": "SUSPENDED",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631339939435000000,
      "openDate": 1631476800000,
      "status": "OPEN",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631476915685000000,
      "openDate": 1631477700000,
      "status": "OPEN",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631477521419000000,
      "openDate": 1631477280000,
      "status": "OPEN",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631477832479000000,
      "openDate": 1631477280000,
      "status": "SUSPENDED",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    {
      "timestamp": 1631477833160000000,
      "openDate": 1631477280000,
      "status": "OPEN",
      "betDelay": 3,
      "inPlay": true,
      "complete": true
    },
    {
      "timestamp": 1631486006482000000,
      "openDate": 1631477280000,
      "status": "SUSPENDED",
      "betDelay": 3,
      "inPlay": true,
      "complete": true
    },
    {
      "timestamp": 1631486183103000000,
      "openDate": 1631477280000,
      "status": "CLOSED",
      "betDelay": 3,
      "inPlay": true,
      "complete": true
    }
  ],
  "odds":
  ....
}
```

## 4- Additional data

As i said now the market info from Betfair is complete, but in order to have a complete DB we have to add some info form this file

### Tennis Data
* [TENNIS ADDITIONAL DATA](https://github.com/marcoselva/rawDataConversion/tree/main/excel/TENNIS)
* [TENNIS ADDITIONAL SPECS](https://github.com/marcoselva/rawDataConversion/blob/main/excel/TennisNotes.txt)

| ATP 	| B 	| C 	| D 	| E 	| F 	| G 	| H 	| I 	| J 	| K 	| L 	| M 	| N 	| O 	| P 	| Q 	| R 	| S 	| T 	| U 	| V 	| W 	| X 	| Y 	| Z 	| AA 	| AB 	| AC 	| AD 	| AE 	| AF 	| AG 	| AH 	| AI 	| AJ 	|
|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|
| ATP 	| Location 	| Tournament 	| Date 	| Series 	| Court 	| Surface 	| Round 	| Best of 	| Winner 	| Loser 	| WRank 	| LRank 	| WPts 	| LPts 	| W1 	| L1 	| W2 	| L2 	| W3 	| L3 	| W4 	| L4 	| W5 	| L5 	| Wsets 	| Lsets 	| Comment 	| B365W 	| B365L 	| PSW 	| PSL 	| MaxW 	| MaxL 	| AvgW 	| AvgL 	|
| 1 	| Antalya 	| Antalya Open 	| 1/7/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Basilashvili N. 	| Arnaboldi A. 	| 40 	| 267 	| 1395 	| 206 	| 4 	| 6 	| 7 	| 5 	| 6 	| 1 	|  	|  	|  	|  	| 2 	| 1 	| Completed 	| 1.5 	| 2.5 	| 1.61 	| 2.44 	| 1.67 	| 2.56 	| 1.56 	| 2.42 	|
| 1 	| Antalya 	| Antalya Open 	| 1/7/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Celikbilek A. 	| Zuk K. 	| 309 	| 262 	| 150 	| 209 	| 7 	| 6 	| 7 	| 5 	|  	|  	|  	|  	|  	|  	| 2 	| 0 	| Completed 	| 2.5 	| 1.5 	| 2.63 	| 1.54 	| 2.7 	| 1.55 	| 2.57 	| 1.5 	|
| 1 	| Antalya 	| Antalya Open 	| 1/7/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Ruusuvuori E. 	| Vesely J. 	| 87 	| 67 	| 806 	| 928 	| 6 	| 3 	| 7 	| 6 	|  	|  	|  	|  	|  	|  	| 2 	| 0 	| Completed 	| 1.5 	| 2.5 	| 1.56 	| 2.58 	| 1.63 	| 3.03 	| 1.52 	| 2.53 	|
| 1 	| Antalya 	| Antalya Open 	| 1/7/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Bublik A. 	| Caruso S. 	| 49 	| 76 	| 1090 	| 858 	| 6 	| 3 	| 6 	| 3 	|  	|  	|  	|  	|  	|  	| 2 	| 0 	| Completed 	| 1.61 	| 2.2 	| 1.81 	| 2.09 	| 1.87 	| 2.3 	| 1.72 	| 2.11 	|
| 1 	| Antalya 	| Antalya Open 	| 1/7/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Goffin D. 	| Herbert P.H. 	| 16 	| 83 	| 2555 	| 822 	| 3 	| 6 	| 7 	| 5 	| 6 	| 0 	|  	|  	|  	|  	| 2 	| 1 	| Completed 	| 1.4 	| 2.75 	| 1.46 	| 2.92 	| 1.5 	| 3 	| 1.44 	| 2.78 	|
| 1 	| Antalya 	| Antalya Open 	| 1/7/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Travaglia S. 	| Kecmanovic M. 	| 75 	| 42 	| 869 	| 1328 	| 1 	| 6 	| 6 	| 4 	| 6 	| 0 	|  	|  	|  	|  	| 2 	| 1 	| Completed 	| 2.62 	| 1.44 	| 2.8 	| 1.49 	| 2.85 	| 1.5 	| 2.71 	| 1.45 	|
| 1 	| Antalya 	| Antalya Open 	| 1/8/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Struff J.L. 	| Kotov P. 	| 37 	| 269 	| 1450 	| 205 	| 6 	| 4 	| 6 	| 3 	|  	|  	|  	|  	|  	|  	| 2 	| 0 	| Completed 	| 1.22 	| 4 	| 1.24 	| 4.44 	| 1.27 	| 4.6 	| 1.22 	| 4.16 	|
| 1 	| Antalya 	| Antalya Open 	| 1/8/2021 	| ATP250 	| Indoor 	| Hard 	| 1st Round 	| 3 	| Lamasine T. 	| Gerasimov E. 	| 271 	| 78 	| 204 	| 840 	| 7 	| 6 	| 6 	| 2 	|  	|  	|  	|  	|  	|  	| 2 	| 0 	| Completed 	| 5 	| 1.16 	| 5.74 	| 1.17 	| 5.74 	| 1.22 	| 5.12 	| 1.16 	|


NB: If the match is found in ATP.xlsx under 2021 folder so we place the value:
```json
   "federation": "ATP", 
   "sex": "MALE",
   "season": 2021
```

If found in WTA excel under 2020 folder so:  

```json
   "federation": "WTA", 
   "sex": "FEMALE",
   "season": 2020
```

### Soccer Data

* [SOCCER ADDITIONAL DATA](https://github.com/marcoselva/rawDataConversion/tree/main/excel/SOCCER)
* [SOCCER ADDITIONAL SPECS](https://github.com/marcoselva/rawDataConversion/blob/main/excel/SoccerNotes.txt)

| A 	| B 	| C 	| D 	| E 	| F 	| G 	| H 	| I 	| J 	| K 	| L 	| M 	| N 	| O 	| P 	| Q 	| R 	| S 	| T 	| U 	| V 	| W 	| X 	| Y 	| Z 	| AA 	| AB 	| AC 	| AD 	| AE 	| AF 	| AG 	| AH 	| AI 	| AJ 	| AK 	| AL 	| AM 	| AN 	| AO 	| AP 	| AQ 	| AR 	| AS 	| AT 	| AU 	| AV 	| AW 	| AX 	| AY 	| AZ 	| BA 	| BB 	| BC 	| BD 	| BE 	| BF 	| BG 	| BH 	| BI 	| BJ 	| BK 	| BL 	| BM 	| BN 	| BO 	| BP 	| BQ 	| BR 	| BS 	| BT 	| BU 	| BV 	| BW 	| BX 	| BY 	| BZ 	| CA 	| CB 	| CC 	| CD 	| CE 	| CF 	| CG 	| CH 	| CI 	| CJ 	| CK 	| CL 	| CM 	| CN 	| CO 	| CP 	| CQ 	| CR 	| CS 	| CT 	| CU 	| CV 	| CW 	| CX 	| CY 	| CZ 	| DA 	|
|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|
| Div 	| Date 	| Time 	| HomeTeam 	| AwayTeam 	| FTHG 	| FTAG 	| FTR 	| HTHG 	| HTAG 	| HTR 	| HS 	| AS 	| HST 	| AST 	| HF 	| AF 	| HC 	| AC 	| HY 	| AY 	| HR 	| AR 	| B365H 	| B365D 	| B365A 	| BWH 	| BWD 	| BWA 	| IWH 	| IWD 	| IWA 	| PSH 	| PSD 	| PSA 	| WHH 	| WHD 	| WHA 	| VCH 	| VCD 	| VCA 	| MaxH 	| MaxD 	| MaxA 	| AvgH 	| AvgD 	| AvgA 	| B365>2.5 	| B365<2.5 	| P>2.5 	| P<2.5 	| Max>2.5 	| Max<2.5 	| Avg>2.5 	| Avg<2.5 	| AHh 	| B365AHH 	| B365AHA 	| PAHH 	| PAHA 	| MaxAHH 	| MaxAHA 	| AvgAHH 	| AvgAHA 	| B365CH 	| B365CD 	| B365CA 	| BWCH 	| BWCD 	| BWCA 	| IWCH 	| IWCD 	| IWCA 	| PSCH 	| PSCD 	| PSCA 	| WHCH 	| WHCD 	| WHCA 	| VCCH 	| VCCD 	| VCCA 	| MaxCH 	| MaxCD 	| MaxCA 	| AvgCH 	| AvgCD 	| AvgCA 	| B365C>2.5 	| B365C<2.5 	| PC>2.5 	| PC<2.5 	| MaxC>2.5 	| MaxC<2.5 	| AvgC>2.5 	| AvgC<2.5 	| AHCh 	| B365CAHH 	| B365CAHA 	| PCAHH 	| PCAHA 	| MaxCAHH 	| MaxCAHA 	| AvgCAHH 	| AvgCAHA 	|
| I1 	| 21/08/2021 	| 17:30 	| Inter 	| Genoa 	| 4 	| 0 	| H 	| 2 	| 0 	| H 	| 17 	| 11 	| 8 	| 5 	| 18 	| 7 	| 8 	| 2 	| 1 	| 2 	| 0 	| 0 	| 1.33 	| 5.25 	| 9 	| 1.33 	| 5.5 	| 8.5 	| 1.37 	| 5.25 	| 8 	| 1.36 	| 5.37 	| 9.65 	| 1.35 	| 5 	| 9 	| 1.3 	| 5 	| 10 	| 1.4 	| 5.5 	| 10 	| 1.35 	| 5.16 	| 8.94 	| 1.66 	| 2.2 	| 1.67 	| 2.33 	| 1.71 	| 2.38 	| 1.63 	| 2.28 	| -1.25 	| 1.75 	| 2.05 	| 1.81 	| 2.11 	| 1.87 	| 2.13 	| 1.8 	| 2.07 	| 1.28 	| 5.75 	| 11 	| 1.3 	| 5.25 	| 10.5 	| 1.3 	| 5.25 	| 11 	| 1.31 	| 5.78 	| 11.37 	| 1.29 	| 5.5 	| 11 	| 1.25 	| 5.75 	| 11.5 	| 1.35 	| 6.25 	| 12.75 	| 1.29 	| 5.58 	| 10.84 	| 1.61 	| 2.3 	| 1.61 	| 2.45 	| 1.7 	| 2.55 	| 1.62 	| 2.32 	| -1.5 	| 1.88 	| 2.05 	| 1.89 	| 2.03 	| 1.96 	| 2.09 	| 1.86 	| 2.01 	|
| I1 	| 21/08/2021 	| 17:30 	| Verona 	| Sassuolo 	| 2 	| 3 	| A 	| 0 	| 1 	| A 	| 12 	| 15 	| 4 	| 8 	| 11 	| 12 	| 7 	| 4 	| 3 	| 2 	| 1 	| 0 	| 2.62 	| 3.3 	| 2.62 	| 2.55 	| 3.5 	| 2.7 	| 2.6 	| 3.45 	| 2.7 	| 2.66 	| 3.55 	| 2.75 	| 2.6 	| 3.4 	| 2.7 	| 2.63 	| 3.25 	| 2.7 	| 2.74 	| 3.55 	| 2.79 	| 2.61 	| 3.43 	| 2.69 	| 1.9 	| 2.03 	| 1.87 	| 2.04 	| 1.9 	| 2.06 	| 1.85 	| 1.98 	| 0 	| 1.93 	| 2 	| 1.93 	| 1.99 	| 1.95 	| 2.01 	| 1.91 	| 1.97 	| 2.5 	| 3.4 	| 2.75 	| 2.55 	| 3.5 	| 2.7 	| 2.55 	| 3.35 	| 2.75 	| 2.64 	| 3.43 	| 2.84 	| 2.5 	| 3.4 	| 2.8 	| 2.55 	| 3.25 	| 2.8 	| 2.75 	| 3.5 	| 2.9 	| 2.57 	| 3.4 	| 2.76 	| 1.8 	| 2 	| 1.81 	| 2.1 	| 1.87 	| 2.17 	| 1.8 	| 2.03 	| 0 	| 1.88 	| 2.05 	| 1.89 	| 2.04 	| 2 	| 2.07 	| 1.86 	| 2.02 	|
| I1 	| 21/08/2021 	| 19:45 	| Empoli 	| Lazio 	| 1 	| 3 	| A 	| 1 	| 3 	| A 	| 16 	| 8 	| 5 	| 5 	| 13 	| 10 	| 5 	| 3 	| 2 	| 1 	| 0 	| 0 	| 4.6 	| 4 	| 1.7 	| 4.6 	| 3.9 	| 1.75 	| 4.6 	| 3.95 	| 1.7 	| 5.01 	| 4.02 	| 1.74 	| 4.75 	| 3.7 	| 1.75 	| 5 	| 3.7 	| 1.7 	| 5.01 	| 4.03 	| 1.79 	| 4.71 	| 3.9 	| 1.73 	| 1.72 	| 2.1 	| 1.75 	| 2.19 	| 1.78 	| 2.21 	| 1.72 	| 2.15 	| 0.75 	| 1.98 	| 1.95 	| 1.97 	| 1.94 	| 2 	| 2 	| 1.93 	| 1.93 	| 3.75 	| 3.8 	| 1.9 	| 4 	| 3.75 	| 1.87 	| 3.65 	| 3.75 	| 1.95 	| 4.11 	| 3.84 	| 1.93 	| 4 	| 3.7 	| 1.88 	| 4 	| 3.6 	| 1.9 	| 4.5 	| 3.94 	| 2 	| 4.06 	| 3.77 	| 1.88 	| 1.66 	| 2.2 	| 1.69 	| 2.29 	| 1.74 	| 2.39 	| 1.68 	| 2.21 	| 0.5 	| 2 	| 1.93 	| 2 	| 1.93 	| 2.06 	| 1.95 	| 1.99 	| 1.88 	|
| I1 	| 21/08/2021 	| 19:45 	| Torino 	| Atalanta 	| 1 	| 2 	| A 	| 0 	| 1 	| A 	| 19 	| 6 	| 8 	| 2 	| 17 	| 13 	| 5 	| 1 	| 2 	| 2 	| 0 	| 0 	| 5.5 	| 4.33 	| 1.55 	| 5 	| 4.25 	| 1.62 	| 5.25 	| 4.3 	| 1.6 	| 5.5 	| 4.25 	| 1.65 	| 5.5 	| 4.2 	| 1.6 	| 5.75 	| 4.2 	| 1.55 	| 5.75 	| 4.48 	| 1.65 	| 5.43 	| 4.23 	| 1.6 	| 1.57 	| 2.37 	| 1.61 	| 2.46 	| 1.61 	| 2.52 	| 1.57 	| 2.43 	| 1 	| 1.89 	| 2.04 	| 1.88 	| 2.06 	| 1.92 	| 2.07 	| 1.87 	| 2 	| 6 	| 4.5 	| 1.5 	| 6.25 	| 4.5 	| 1.5 	| 6 	| 4.5 	| 1.53 	| 6.51 	| 4.5 	| 1.54 	| 6.5 	| 4.2 	| 1.53 	| 6.5 	| 4.33 	| 1.5 	| 6.9 	| 4.75 	| 1.59 	| 6.16 	| 4.48 	| 1.52 	| 1.53 	| 2.5 	| 1.55 	| 2.6 	| 1.63 	| 2.72 	| 1.56 	| 2.45 	| 1 	| 2.06 	| 1.87 	| 2.08 	| 1.85 	| 2.19 	| 1.9 	| 2.03 	| 1.84 	|
| I1 	| 22/08/2021 	| 17:30 	| Bologna 	| Salernitana 	| 3 	| 2 	| H 	| 0 	| 0 	| D 	| 18 	| 8 	| 7 	| 4 	| 13 	| 15 	| 9 	| 4 	| 6 	| 3 	| 2 	| 1 	| 1.65 	| 4 	| 5 	| 1.67 	| 4 	| 5 	| 1.63 	| 4.1 	| 5.25 	| 1.65 	| 4.29 	| 5.42 	| 1.63 	| 4 	| 5.25 	| 1.62 	| 3.75 	| 5.75 	| 1.7 	| 4.29 	| 5.75 	| 1.65 	| 4.04 	| 5.15 	| 1.8 	| 2 	| 1.8 	| 2.11 	| 1.87 	| 2.11 	| 1.81 	| 2.02 	| -0.75 	| 1.85 	| 2.08 	| 1.84 	| 2.1 	| 1.88 	| 2.1 	| 1.83 	| 2.05 	| 1.5 	| 4.5 	| 6 	| 1.53 	| 4.4 	| 6 	| 1.55 	| 4.3 	| 5.75 	| 1.55 	| 4.52 	| 6.38 	| 1.52 	| 4.33 	| 6.5 	| 1.5 	| 4.2 	| 7 	| 1.59 	| 4.61 	| 7 	| 1.54 	| 4.37 	| 6.05 	| 1.72 	| 2.1 	| 1.72 	| 2.24 	| 1.76 	| 2.37 	| 1.7 	| 2.16 	| -1 	| 1.94 	| 1.99 	| 1.92 	| 2.01 	| 2.02 	| 2.01 	| 1.91 	| 1.95 	|
| I1 	| 22/08/2021 	| 17:30 	| Udinese 	| Juventus 	| 2 	| 2 	| D 	| 0 	| 2 	| A 	| 11 	| 11 	| 6 	| 4 	| 11 	| 12 	| 3 	| 3 	| 1 	| 3 	| 0 	| 0 	| 7.5 	| 4.33 	| 1.45 	| 7.5 	| 4.5 	| 1.44 	| 7.5 	| 4.4 	| 1.45 	| 7.59 	| 4.48 	| 1.49 	| 7.5 	| 4.2 	| 1.47 	| 8 	| 4.33 	| 1.4 	| 8 	| 4.5 	| 1.53 	| 7.21 	| 4.35 	| 1.47 	| 1.72 	| 2.1 	| 1.79 	| 2.13 	| 1.82 	| 2.15 	| 1.77 	| 2.08 	| 1 	| 2.05 	| 1.75 	| 2.15 	| 1.79 	| 2.15 	| 1.86 	| 2.08 	| 1.79 	| 7 	| 4 	| 1.5 	| 5.75 	| 4.2 	| 1.57 	| 6.75 	| 4.1 	| 1.53 	| 7.45 	| 4.03 	| 1.56 	| 7 	| 4.2 	| 1.5 	| 7.5 	| 3.9 	| 1.5 	| 8.08 	| 4.25 	| 1.59 	| 6.89 	| 4.03 	| 1.53 	| 2.09 	| 1.84 	| 2.08 	| 1.83 	| 2.13 	| 1.95 	| 1.98 	| 1.85 	| 1 	| 1.91 	| 1.99 	| 1.93 	| 1.99 	| 2.01 	| 2 	| 1.93 	| 1.93 	|
| I1 	| 22/08/2021 	| 19:45 	| Napoli 	| Venezia 	| 2 	| 0 	| H 	| 0 	| 0 	| D 	| 13 	| 8 	| 4 	| 4 	| 5 	| 22 	| 2 	| 2 	| 1 	| 7 	| 1 	| 0 	| 1.22 	| 6.5 	| 12 	| 1.25 	| 6.25 	| 11 	| 1.25 	| 6.5 	| 11 	| 1.25 	| 6.67 	| 12.08 	| 1.24 	| 6 	| 13 	| 1.2 	| 6.5 	| 13 	| 1.28 	| 6.8 	| 13 	| 1.24 	| 6.38 	| 11.79 	| 1.44 	| 2.75 	| 1.44 	| 2.91 	| 1.48 	| 2.95 	| 1.44 	| 2.78 	| -1.75 	| 1.89 	| 2.04 	| 1.87 	| 2.05 	| 1.9 	| 2.05 	| 1.86 	| 2.02 	| 1.2 	| 6.5 	| 13 	| 1.22 	| 6.75 	| 12 	| 1.22 	| 6.75 	| 12 	| 1.22 	| 7.1 	| 13.81 	| 1.2 	| 6.5 	| 15 	| 1.18 	| 6.5 	| 17 	| 1.25 	| 7.25 	| 17 	| 1.22 	| 6.74 	| 12.94 	| 1.4 	| 3 	| 1.43 	| 2.98 	| 1.46 	| 3 	| 1.42 	| 2.87 	| -2 	| 2.04 	| 1.89 	| 2.03 	| 1.88 	| 2.15 	| 1.99 	| 2.03 	| 1.84 	|
| I1 	| 22/08/2021 	| 19:45 	| Roma 	| Fiorentina 	| 3 	| 1 	| H 	| 1 	| 0 	| H 	| 11 	| 11 	| 6 	| 8 	| 12 	| 14 	| 4 	| 4 	| 3 	| 2 	| 1 	| 1 	| 1.72 	| 3.8 	| 4.75 	| 1.72 	| 4 	| 4.6 	| 1.75 	| 3.95 	| 4.3 	| 1.81 	| 3.96 	| 4.59 	| 1.75 	| 3.8 	| 4.6 	| 1.73 	| 3.7 	| 4.75 	| 1.82 	| 4.03 	| 4.75 	| 1.77 	| 3.85 	| 4.5 	| 1.66 	| 2.2 	| 1.72 	| 2.23 	| 1.76 	| 2.25 	| 1.68 	| 2.2 	| -0.75 	| 2.02 	| 1.91 	| 2.02 	| 1.9 	| 2.02 	| 1.93 	| 1.99 	| 1.88 	| 1.6 	| 4.2 	| 5.25 	| 1.6 	| 4.33 	| 5.25 	| 1.63 	| 4.2 	| 4.9 	| 1.67 	| 4.2 	| 5.31 	| 1.61 	| 4 	| 5.5 	| 1.6 	| 4 	| 5.5 	| 1.71 	| 4.4 	| 5.6 	| 1.65 	| 4.16 	| 5.11 	| 1.61 	| 2.3 	| 1.61 	| 2.44 	| 1.68 	| 2.55 	| 1.61 	| 2.33 	| -0.75 	| 1.85 	| 2.08 	| 1.85 	| 2.08 	| 1.86 	| 2.16 	| 1.82 	| 2.06 	|

#### TABLE FOR LEAGUE

In addition for soccer we should set the division value based on column A in the found match line

ex: Inter v Juvents -> find in file called I1 under folder 2021-> we put this value in addition football info

```json
  "league": "Serie A",
  "countryCode": "ITA",
  "season": "2020/2021",
```

Based on this code list

| # 	| code ( columns a in excel, named DIV) 	| leagueName 	| countryCode 	|
|---	|---	|---	|---	|
| 1 	| E0 	| Premier League 	| GBR 	|
| 2 	| E1 	| Championship 	| GBR 	|
| 3 	| SC0 	| Premier League 	| SCOT 	|
| 4 	| SC1 	| Division 1 	| SCOT 	|
| 5 	| D1 	| Budesliga 1 	| GER 	|
| 6 	| D2 	| Budesliga 2 	| GER 	|
| 7 	| I1 	| Serie A 	| ITA 	|
| 8 	| I2 	| Serie B 	| ITA 	|
| 9 	| SP1 	| La Liga Primera Division  	| ESP 	|
| 10 	| SP2 	| La Liga Segunda Division 	| ESP 	|
| 11 	| F1 	| Ligue 1 	| FRA 	|
| 12 	| F2 	| Ligue 2 	| FRA 	|
| 13 	| N1 	| Eredivise 	| NLD 	|
| 14 	| B1 	| Jupiler League  	| BEL 	|
| 15 	| P1 	| Liga I 	| PRT 	|
| 16 	| T1 	| Futbol Ligi 1  	| TUR 	|
| 17 	| G1 	| Ethniki Katigoria 	| GRE 	|


### HORSE: 
 no additional info to add

The task should check in the excel or csv file if the market is present (it's possible that not exist in excel DB)
If not presnt in db set

```json
 "additionalInfo":{
  "tennis": null,
  "soccer": null,
  "horse": null,
 }                                 
```  

looking by marketName, runner name and date we should find the market in the .csv / .excel

After found the correct line in excel/csv we should add this data in the market info.

NB: I didn't make this part in my code, you have to start from 0. 
I can suggest you to search in excel the name of the runners in the columns together with the date (a market with 2 same runners and particular date is always unique) and then copy the data.


At end of this proces the complete file should look like this ( marketUpdates ans odds part are ommised)

```json

{
  "info": {
    "id": "1.187528277",
    "eventId": 30891863,
    "eventName": "Match Odds",
    "marketType": "MATCH_ODDS",
    "openDate": 1631477833160,
    "name": "Djokovic v Medvedev",
    "numberOfActiveRunner": 2,
    "countryCode": "US",
    "sport": "TENNIS",
    "venue": "",
    "volume": {
      "total": 11825068.38,
      "preMatch": 1852569.96,
      "inPlay": 9972498.42
    },
    "winner": {
      "id": 19924831,
      "name": "Daniil Medvedev",
      "status": "WINNER",
      "position": 2
    },
    "delay": 3
  },
  "runners": [
    {
      "id": 2249229,
      "name": "Novak Djokovic",
      "status": "LOSER",
      "position": 1,
      "inPlayOdds": 1.44,
      "inPlayTime": 1631477833160,
      "avgPrematch": 1.42,
      "closedOdds": 19.0,
      "maxPrematch": 1.44,
      "minPrematch": 1.38,
      "maxInPlay": 120.0,
      "minInPlay": 1.41,
      "inPlayIndex": 4532,
      "lengthOdds": 12014,
      "lengthOddsPrematch": 4532,
      "lengthOddsInPlay": 7482,
      "tradedVolume": 4302965.3,
      "preMatchVolume": 1578301.23,
      "inPlayVolume": 2724664.07
    },
    {
      "id": 19924831,
      "name": "Daniil Medvedev",
      "status": "WINNER",
      "position": 2,
      "inPlayOdds": 3.3,
      "inPlayTime": 1631477833160,
      "avgPrematch": 3.34,
      "closedOdds": 1.01,
      "maxPrematch": 3.55,
      "minPrematch": 3.25,
      "maxInPlay": 3.45,
      "minInPlay": 1.01,
      "inPlayIndex": 3013,
      "lengthOdds": 10613,
      "lengthOddsPrematch": 3013,
      "lengthOddsInPlay": 7600,
      "tradedVolume": 7522103.08,
      "preMatchVolume": 274268.73,
      "inPlayVolume": 7247834.35
    }
  ],
  "marketUpdates": [
    {
      "timestamp": 1631330837213000000,
      "openDate": "2021-09-12T15:00:00.000Z",
      "status": "OPEN",
      "betDelay": 0,
      "inPlay": false,
      "complete": true
    },
    ....

  ],
  "additionalInfo":{                                            // data added via excel
      "tennis":{                                                // only for TENNIS, otherwise null
            "tennisTournament":{
                "location":  "New York",                // columns B
                "tournament":  "US Open",               // columns C
                "series":  "Grand Slam",                // columns E
                "court": "Outdoor",                     // columns F
                "surface":  "Hard",                     // columns G
                "round":   "The Final",                 // columns H
                "bestOf":  5                           // columns I
            },
            "tennisRank": {
                "winnerRank": 2,                       // columns L
                "winnerPoint": 9980,                    // columns N
                "loserRank":  1,                       // columns M
                "loserPoint": 11113                    // columns O
            },
            "finalResult":{
                "winner": {
                    "s1": 6,                           // columns P
                    "s2": 6,                           // columns R
                    "s3": 6,                           // columns T
                    "s4": null,                        // columns V
                    "s5": null,                        // columns X
                    "totalSet": 3                      // columns Z
                },
                "loser": {
                    "s1": 4,                           // columns Q
                    "s2": 4,                           // columns S
                    "s3": 4,                           // columns U
                    "s4": null,                        // columns W
                    "s5": null,                        // columns Y
                    "totalSet": 0                       // columns AA
                },
                "comment": "Completed"                   // columns AB
            },
             "bookOdds": {
                "bet365":{
                    "winner": 1.4,                         // columns AC
                    "loser": 3,                            // columns AD
                },
                "pinnacle":{
                    "winner": 1.42,                        // columns AE
                    "loser": 3.14,                         // columns AF
                },
                "maxOddsPortal": {
                    "winner": 1.45,                        // columns AG
                    "loser": 3.36,                         // columns AH
                },
                "avgOddsPortal": {
                    "winner": 1.39,                        // columns AI
                    "loser": 4,                            // columns AJ
                }
            }
      },
      "football":{                                     // only for SOCCER, otherwise null. This data is based on Inter v Genoa -21/08/2021
            "league": "Serie A",                      // added previously based on wher path and file found the market
            "countryCode": "ITA",                      // added previously based on wher path and file found the market
            "season": "2020/2021",                       // added previously based on wher path and file found the market                  
            "finalResult":{
                "home": {
                    "fthg": 4,                         // Full Time Home Team Goals -  columns F
                    "hthg": 2,                         // Half Time Home Team Goals -  columns I
                },
                "away": {
                    "ftag": 0,                         // Full Time Away Team Goals -  columns G
                    "htag": 0,                         // Half Time Away Team Goals -  columns J
                },
                "ftr": "H",                              // Full Time Result (H=Home Win, D=Draw, A=Away Win) - columns H
                "htr": "H"                               // Half Time Result (H=Home Win, D=Draw, A=Away Win) - columns K
            },
            "matchStats": {
                "hs": 17,                               // Home Team Shots - columns L
                "as": 11,                               // Away Team Shots - columns M
                "hst": 8,                               // Home Team Shots on Target - columns N
                "ast": 5,                               // Away Team Shots on Target - columns O
                "hhw": null,                            // Home Team Hit Woodwork - columns --
                "ahw": null,                            // Away Team Hit Woodwork - columns --
                "hc": 8,                                // Home Team Corners - columns R
                "ac": 2,                                // Away Team Corners - columns S
                "hf": 18,                               // Home Team Fouls Committed - columns P
                "af": 7,                                // Away Team Fouls Committed - columns Q
                "hfkc": null,                           // Home Team Free Kicks Conceded - columns --
                "afkc": null,                           // Away Team Free Kicks Conceded - columns --
                "ho": null,                             // Home Team Offsides - columns --
                "ao": null,                             // Away Team Offsides - columns --
                "hy": 1,                                // Home Team Yellow Cards - columns T
                "ay": 3,                                // Away Team Yellow Cards - columns U
                "hr": 0,                                // Home Team Red Cards - columns V
                "ar": 0,                                // Away Team Red Cards - columns W
            },
             "bookOdds": {
                "bet365":{
                    "matchOdds": {
                        "home": 1.33,                         // B365H - columns X
                        "draw": 5.25,                         // B365D - columns Y
                        "away": 9,                           //  B365A - columns Z
                    },
                    "uo25": {
                        "under25": 2.2,                       //B365<2.5 -  columns AW
                        "over25": 1.66,                       //B365>2.5 - columns AV
                    }
                },
                "pinnacle":{
                    "matchOdds": {
                        "home": 1.36,                         // PSH - columns AG
                        "draw": 5.37,                         // PSD - columns AH
                        "away": 9.65,                         // PSA - columns AHI
                    },
                    "uo25": {
                        "under25": 2.33,                       // P<2.5 - columns AX
                        "over25": 1.67,                        // P>2.5 - columns AY
                    }
                }
            }
      },
  },
}


```

## 5- check and save JSON

Now we should check that the json file is correct and consistent and not miss any part.

Now that the markert JSON is complete we can save that in `code/exportOutput/markets` (for the moment it save all togheter but we can mantain the original path, so divided by sport and types)

* `code/exportOutput/markets/BASIC/SOCCER`
* `code/exportOutput/markets/BASIC/TENNIS`
* `code/exportOutput/markets/BASIC/HORSE RACING`
----------------------------
* `code/exportOutput/markets/ADVANCED/SOCCER`
* `code/exportOutput/markets/ADVANCED/TENNIS`
* `code/exportOutput/markets/ADVANCED/HORSE RACING`

## 6- check and generate RunnerDB

We should start to generate the runnersDB JSON, saving all runners present in the market already saved.

In order to do that we have to save form markets info in runners props
* id: id of the runner
* name: name of the runner


```python

    # ##
    #  --- RUNNERS DB CREATOR ---
    # ##
    print('\n\n------ 4 -GENEREATE RUNNERS INFO------')
    runnersDB = RunnersDB()
    for marketList in marketList:
        runnersDB.saveRunnersOfMarket(marketList)
```
NB: don't add duplicate runner or runners id that already present in the list

Example:
```json
[{"id": 35900675, "name": "Youllovemewheniwin"}, 
{"id": 36764551, "name": "Kaths Toyboy"}, 
{"id": 750247, "name": "Strike"}, 
{"id": 28602170, "name": "Hyde Park Barracks"}, 
{"id": 39258079, "name": "Mr Professor"},
....
]
```

We should save the JSON list with this filename `code/exportOutput/runner/runnerDB_CURRENTDATE`

----------------------------

<b>Fell free to write me if you have some problems to understand this documentation or the code</b>
















