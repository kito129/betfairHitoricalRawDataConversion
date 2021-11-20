
AT THE END OF THE PROCESS THE DATA SHOULD BE LIKE this

for the data we take the last market update in cronological order

```json
{
  "marketId":  "1.187528277",                           // marketId of the event             
  "info": {         
    "eventId":  "30891863",                            // = eventId
    "eventName":  "Match Odds",                         // = eventName    
    "marketType":   "MATCH_ODDS",                       // = marketType       
    "openDate":  1631477832479,                        // is September 12, 2021 8:17:12.479 PM (as we can check with suspension error) and not September 12, 2021 8:08:08.000 as the data say
    "name":  "Djokovic v Medvedev",                     // = eventName
    "numberOfActiveRunner": 2,                         // = numberOfActiveRunner
    "countryCode": "US",                              // = countryCode, possible NULL
    "sport":  "TENNIS",                                // sport is detected by initial folder name                           
    "venue": "",                                      // = venue, possible NULL, works only for horse races                          
    "tradedVolume": {           
      "total": 11825068.379999999,                     // total tradedVolume volume on all selections = sum of last tv for each selections
      "preMatch": 784775.1900000001,                   // total tradedVolume volume on all selections until market is not started = sum of tv for each selections until market is not starte
      "inPlay": 11040293.19                            // total tradedVolume volume on all selections from market start = sum of tv for each selections from market start - preMatch for each selection
    },
    "winner": {                     
      "id": 19924831,                                 // winner id
      "name": "Daniil Medvedev",                      // winner name         
    },      
    "inPlayDelay":  3,                                 // betDelay
  },
  "selections": {
    "runners": [
      {
        "id": 2249229,                     
        "name": "Novak Djokovic",
        "status":  "LOSER",
        "position":  1,
        "preMatch":{                                            // before market start (openDate of market)
            "avg":  1.42,                              // mean of all ltp before market starts
            "firstOdds":  1.44,                        // first cronological ltp
            "maxPrematch": 1.44,                                // max reach before market starts
            "minPrematch": 1.38,                                // min reach before market starts
        },
        "inPlay":{
            "inPlayTime":  1631470086469,              // inplay time for selection
            "inPlayIndex": 2879,                                // first inplay traded price index
            "bsp":  1.42,                              // first inplay traded price
            "lastOdds": 19.0,                                   // last cronological ltp
            "maxInPlay": 120.0,                                 // max reach after market starts                        
            "minInPlay": 1.41,                                  // mini reach after market starts                                    
        
        },
        "data": {
            "lengthOdds": 12014,                                // total prices updates
            "lengthOddsPrematch": 2879,                         // total prices updates before market start
            "lengthOddsInPlay": 9135,                           // total prices updates after market start
        } ,
        "tradedVolume": {
            "total": 4302965.3,                                 // total traded volume on this selection
            "preMatch": 652080.65,                              // total traded volume on this selection before market start
            "inPlay": 3650884.65                                // total traded volume on this selection after market start
        }
      },
      {
        "id": 19924831,                               
        "name": "Daniil Medvedev",
        "status": "WINNER",
        "position":  2,
        "preMatch":{
            "avg":  3.36,
            "firstOdds":  3.28,
            "maxPrematch": 3.55,
            "minPrematch": 3.25,
        },
        "inPlay":{
            "inPlayTime":  1631470134432,
            "bsp":  3.3,
            "lastOdds": 1.01,
            "maxInPlay": 3.45,
            "minInPlay": 1.01,
            "inPlayIndex": 2014,
        },
        "data": {
            "lengthOdds": 10613,
            "lengthOddsPrematch": 2014,
            "lengthOddsInPlay": 8599,
        } ,
        "tradedVolume": {
            "total": 7522103.08,
            "preMatch": 132694.54,
            "inPlay":  7389408.54
        }
      },
    ]
  },
  "prices":{
    "selection":[
        {
            "selectionId": 2249229,
            "odds": [
            {
                "timestamp": 1631331869016,                         // time stamp of prices updates
                "ltp": 1.44,                                        // Last Traded Price - the last price the runner traded at.
                "tv": 88.67,                                        // Traded Volume - The total amount matched on the runner 
                "trd": [                                            // Traded PriceVol tuple delta of price changes (0 vol is remove)
                    [
                        1.44,
                        88.67
                    ]
                ],
                "batb": [                                // batb: best available to back - LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove). 
                    [0, 3, 9],
                    [1, 2.88, 20],
                    [2, 2.14, 50]
                ],
                "batl": [                             // batl: best available to lay - LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove). 
                    [0, 1.15, 50.42],
                    [1, 1.2, 79],
                    [2, 1.3, 43.7 ]
                ],
            },
            {...}
            ......
            ]
        },
        {
            "selectionId": 19924831,
            "odds": [
            {
                ....
            },
            ]
        }
    ]
  }
}
```