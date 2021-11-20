 COMPLETE DATA - V1 // ONLY EXCEL DATA
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
    "countryCode":   "US",                              // = countryCode, possible NULL
    "sport":   "TENNIS",                                // sport is detected by algoritm (1)
    "venue":   "",                                      // = venue, possible NULL, works only for horse races
    "tradedVolume": {
      "total": 11825068.37,                            // total tradedVolume volume on all selections = sum of last tv for each selections
      "preMatch": 784775.19,                           // total tradedVolume volume on all selections until market is not started = sum of tv for each selections until market is not starte
      "inPlay": 11040293.19                            // total tradedVolume volume on all selections from market start = sum of tv for each selections from market start - preMatch for each selection
    },
    "winner": {
      "id":   19924831,                                 // winner id
      "name":   "Daniil Medvedev",                      // winner name
    },
    "inPlayDelay":  3,                                 // betDelay
  },
  "selections": {
    "runners": [
      {
        "id": 2249229,
        "name": "Novak Djokovic",
        "status": "LOSER",
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
        },
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
        },
        "tradedVolume": {
            "total": 7522103.08,
            "preMatch": 132694.54,
            "inPlay":  7389408.54
        }
      },
    ]
  },
  "additionalInfo":{                                            // data added via excel
      "tennis":{                                                // if is not tennis is null
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
      "football":{                                              // if is not football is null, this data is based on Inter v Genoa -21/08/2021
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
  "prices":{
    "selection":[
        {                                                           // one for each selection
            "selectionId": 2249229,                        // selectionId of odds
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
                "batl":  [                             // batl: best available to lay - LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove).
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
```