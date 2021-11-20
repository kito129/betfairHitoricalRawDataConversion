<br />
<div align="center">

  <h3 align="center">DB SPECIFICATION</h3>

  <p align="center">
    A formal specification of raw data, tre process to convert data to obtain myJSON object and final population of DB
  </p>
</div>


## Raw Data definition

* [Betfair Docs](https://github.com/marcoselva/BFplatform/blob/main/01_dbCreation/Betfair-Historical-Data-Feed-Specification.pdf)

The database on which we will operate will be purchased from betfair exchange and will include all the matches on the platform, with information about 
* The event information
* The market updates (event open, inPlay, closed..).
* The runners (the competitors of the event) 
* The odds (price, volume and available prices).

This is a sample of market Djokovic v Medvedev of 12/09/2021

[`sampleADVANCED.json`](https://github.com/marcoselva/BFplatform/blob/main/01_dbCreation/rawData/sampleADVANCED.json)

As you can see this is a list of Market change in the time (pt is published time), and the main propose is to convert this time data in
* A single version of market info (event, name, time, open date and all info about the market) -> from now on we will call it <b> MarketInfo</b>
* A single version of market runners,  All info about selection of the markets (id, name, position...) -> from now on we will call it <b> MarketSelections</b>
* The odds information during the time about all selection in the market (time of update, price, volume and available prices...) -> from now on we will call it <b> MarketPrices</b>
* The update of the market during the time (open, suspended market, in play, event start, event closed...) -> from now on we will call it <b> MarketUpdates</b>


As you can see there are two types of data:
* BASIC
* ADVANCED
Both contain the same information, but ADVANCED has updates every second and complex odds data (time, odds, traded volume, available to bet) while BASIC has updates every minute and the only odds information is time and last traded.

The purpose of the code to be created would be to be able to interpret both types of data, and automatically determine whether it is ADVANCED or BASIC
Then create in the db the occurrences found and then define for that market UNIQUE:

* Market Info 
* Market Selection

While two separate enities for 

* MarketBasicUpdates
* MarketBasicPrices

* MarketAdvancedUpdates
* MarketAdvancedPrices

So as to be able to search for events and selections in a unique way, and then display, according to availability, only BASIC, only ADVANCED or both types of data.


## Download data and Extract principal ZIP

The first process to do is download the data form [Betfair](https://historicdata.betfair.com/#/home)
This process includes purchase and authentication task, so i don't want to automate that process.

I will provide you a sample of data to working about.
Then i will use for my self the code over all data to create my personal db.

The code should be run once a day, as the data is released after 5 days from the end of the event.
So this code will need to be run once a day to add the newly downloaded markets to the DB.

## Extract All market

The situation before starting the code would be:

I put all the .bz2 archive in this folders

`dataToAdd/BASIC/football/`
`dataToAdd/BASIC/tennis/`
`dataToAdd/BASIC/horseracing/`

`dataToAdd/ADVANCED/football/`
`dataToAdd/ADVANCED/tennis/`
`dataToAdd/ADVANCED/horseracing/`

From here we hould extract the bz2 and save as json

I created this code, that you have to fix

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
    countFile = 0
    countOK = 0
    for (dirpath, dirnames, files) in os.walk(dataPath):
        for fileName in files:
            # filter out decompressed files
            if fileName.endswith('.json'):
                countFile = countFile + 1
                continue

            # save file as .json
            filepath = os.path.join(dirpath, fileName)
            newFilepath = extractPath + fileName + '.json'
           

            # save JSON file
            with open(newFilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
                countOK = countOK + 1
                for data in iter(lambda: file.read(), b''):
                    new_file.write(data)
            file.close()
            countOK = countOK +1

    # print recap
    print("File to extract: " + str(countFile))
    print("OK Extracted: " + str(countOK))
    print('\nEnd of extraction..\n')


```

At the end of this process we could have a folder ( at the moment i didn't implement the sport division)

`pythonCode/historicJSON/BASIC/football/`
`pythonCode/historicJSON/BASIC/tennis/`
`pythonCode/historicJSON/BASIC/horseracing/`

`pythonCode/historicJSON/ADVANCED/football/`
`pythonCode/historicJSON/ADVANCED/tennis/`
`pythonCode/historicJSON/ADVANCED/horseracing/`

contains all data convertet to JSON

In a folder all market downloaded and converted in correct JSON, as: `1.187528277_ADVANCED.json` or `1.187528277_BASIC.json`
the current code save the file without BASIC or ADVANCED prefix and  we should change that in order to analyze at the same time both ADVANCED and BASIC markets (they have the same market ID so they are separated)
 
## Convert to JSONv1

Now start the real conversion task.

`pythonCode/dataframe.py` is were i placed the code that made this division and create an object like this


First in my version i convert this `1.1.187528277_ADVANCED.json` to a panda dataframe in order to separate all lines and save the pt (publish time in milliseconds UTC)

There will be 2 different types of line

MARKET UPDATE

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
        "eventId": "30891863",
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
        "eventName": "Djokovic @ Medvedev"
      }
    }
  ]
}
  ```
ODDS UPDATE
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
      ],
      "tv": 19833.28
    }
  ]
}
```

At the end of proces we could have this division

```python
mainObj = {
  'market': getMarketDataframe(path),
  'runners': getRunnerDataframe(path),
  'odds': getPricesDataframe(path, status)
}
```

  This is an example of data contained

`mainObj['market"]`

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


NOTE: for market update we should remove the identical update (line with no changes except "version" value )

this is my code to that
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

`mainObj['market"]` // removed identical lines ( exepct version)

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


`mainObj['runners"]`

|     | status   |       id | name            |   sortPriority |
|----:|:---------|---------:|:----------------|---------------:|
| 140 | LOSER    |  2249229 | Novak Djokovic  |              1 |
| 141 | WINNER   | 19924831 | Daniil Medvedev |              2 |


`mainObj['odds"]` // some lines are removed


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


Now we have completed conversion from original file to panda dataframe

Now at line 65 of `pythonCode/main.py` we should have this mainObj


It' the moment to start to convert in python object

i pass this obj to convertToMyObject(dataframe, path, status) function tha is in `pythonCode/dfToObeject.py`

in this file i separate MarketInfo, MarketSelection, MarketUpdates, MarketPrices entities and i covert panda df to python obj

at the line 35 of `pythonCode/dfToObeject.py` i start to create MarketInfo

The class is defined in `pythonCode/object/markets.py` 
The constructor take the dataframe and create a python object based on last market update (line 18 in `pythonCode/object/markets.py`)

I take into consideration the last update to be sure to get the complete info (based on the fact that they are the info on which will be based the settlement of the market and then its closing)

Now at line 51 we start with match update fix

In practice there is an "error" on the data reported by betfair. The starting time reported in the market update (openDate) is almost never correct to the thousandth because that value (openDate) is set according to the official time of, but then the match starts at a different time (sometimes we talk about a few seconds or minutes, while in other cases the deviation can be much larger.

To correct this error there are two different ways:

1)

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



like here as you can see betfair report for open date  2021-09-12T20:08:00.000Z, but the correct in play time is 2021-09-12 20:17:13.160000, and we can find it iterating over the marketUpdate array and stopping the search when these conditions are all true:

* status = OPEN
* inPlay = TRUE
* betDelay > 0


something  like this 
```python
inPlayTime = 0
#find open time for market Update
for elem in self.marketUpdates:
    if elem['inPlay'] and elem['status'] == 'OPEN' and elem['betDelay'] >0 :
        inPlayTime = int(elem['timestamp'])
        break
``` 

Now we can save the info about betDelay
There are some rule to remove / skip the market if betDelay are to high

* Tennis --> remove if (betdelay >3 and open date > 2019)
* Tennis --> remove if (betdelay >5 and open date < 2019)
* Football --> remove if betdelay >7


at this stage the object looks like this















