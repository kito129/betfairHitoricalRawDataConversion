it's all ok! great :)

but we still miss some additional info columns

it's ok that you find the market row in the excel but as i said in the main readme.md I need more rich info for all the columns in the find row

for example

SOCCER

/BASIC/SOCCER/2021/SEPT/17/30850656/1.187051652

have only this info 

  ```json
 "additionalInfo": {
        "league": "Premier League",
        "countryCode": "GBR",
        "season": "2021/2022"
    }
```
 
but as i said i need all columns data
once fond the row in excel we need to copy these columns in the JSON

  ```json
 "additionalInfo":{                                     
            "league": "Premier League",                     
            "countryCode": "GBR",                      
            "season": "2021/2022,                                     
            "finalResult":{
                "home": {
                    "fthg": 4,                         // columns F
                    "hthg": 2,                         // columns I
                },
                "away": {
                    "ftag": 0,                         // columns G
                    "htag": 0,                         //columns J
                },
                "ftr": "H",                              // columns H
                "htr": "H"                               //columns K
            },
            "matchStats": {
                "hs": 17,                               // columns L
                "as": 11,                               // columns M
                "hst": 8,                               // columns N
                "ast": 5,                               // columns O
                "hc": 8,                                //  columns R
                "ac": 2,                                //  columns S
                "hf": 18,                               // columns P
                "af": 7,                                //  columns Q
                "hy": 1,                                // columns T
                "ay": 3,                                //  columns U
                "hr": 0,                                //columns V
                "ar": 0,                                //  columns W
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
      
```

note:  since SOCCER events have several markets for the same event, please add the additional info only in the "marketType": "MATCH_ODDS", and leave empty the other marketType



TENNIS

/ADVANCED/TENNIS/2021/SEPT/20/30918523/1.187815108

for the moment have this info 

  ```json
    "additionalInfo": {
        "federation": "ATP",
        "sex": "MALE",
        "season": 2021
    }
  ```
  
but I need all the columns specified

  ```json
"tennis":{         
            "federation": "ATP",
            "sex": "MALE",
            "season": 2021,
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
  ```

