ORIGINAL JSON FORMAT
   ```json
        {
          "op":  "mcm",                                     // market change message                                                                     
          "clk":  "4228571262",                           // sequence number -- IGNORED                                                        
          "pt": 1631486183103,                            // Published Time (in millis since epoch)                                            
          "mc": [                                                   // Market change Changes to runners or market definition                           
            {   
              "id":   "1.187528277",                                                                                  
              "marketDefinition": {                                 // - Fields containing details of the market - update every change              
                "bspMarket":   false,                      // If 'true' the market supports Betfair SP betting                                                                                                     
                "turnInPlayEnabled":   true,               // If 'true' the market is set to turn in-play                           
                "persistenceEnabled":  true,                 // If 'true' the market supports 'Keep' bets if the market is to beturned in-play 
                "marketBaseRate":  5.0,                   // The commission rate applicable to the market                                                                  
                "eventId": "30891863",                       // The unique id for the event 
                "eventTypeId":  "2",                      //IGNORED                             
                "numberOfWinners":  1,                     // The number of winners on a market             
                "bettingType": "ODDS",                      // ODDS,ASIAN_HANDICAP_DOUBLE_LINE,ASIAN_HANDICAP_SINGLE_LINE
                "marketType":   "MATCH_ODDS",               // MACTH_ODDS, U/02.5, BTS...
                "marketTime":   "2021-09-12T20:08:00.000Z", // TO CONVERT IN INTEGER -  market start time NB not always correct, first get the last market update, second chek if happends fast suspension like in tennis match and update
                "suspendTime":  "2021-09-12T20:08:00.000Z", // TO CONVERT IN INTEGER -  market suspend time NB not always correct, is the end of match
                "bspReconciled":   false,                  // IGNORED
                "complete":   true,                        //If false, runners may be added to the maket
                "inPlay":   true,                          // True if the market is currently in play NB inPlay for betfair is not the same of event started, in tennis check for marketTime and every suspension of the market
                "crossMatching":   false,                  // True if cross matching is enabled for this market.
                "runnersVoidable":   false,                // True if runners in the market can be voided 
                "numberOfActiveRunners":  0,              // The number of runners that are currently active. An active runner is a selection available for betting
                "betDelay": 3,                            // The number of seconds an order is held until it is submitted into the market. Orders are usually delayed when the market is inplay 
                "status": "CLOSED",                         // OPEN, SUSPENDED, CLOSED
                "settledTime": "2021-09-12T22:34:27.000Z",   // close time of the market
                "runners": [                                        // Details of the selection in the betting market
                  {
                    "status": "LOSER",                      // ACTIVE, REMOVED, WINNER,PLACED, LOSER, HIDDEN
                    "sortPriority":  1,                    //The sort priority of this runne             
                    "id":  2249229,                        // selectionId of the runner
                    "name":   "Novak Djokovic"              // The name of the runner
                  },
                  {
                    "status": "WINNER",
                    "sortPriority": 2,
                    "id": 19924831,
                    "name": "Daniil Medvedev"
                  }
                ],
                "regulators": [                                     // IGNORED
                  "MR_INT"
                ],
                "countryCode":  "US",                       // Country code of event NB not always works                       
                "discountAllowed":   true,                 // IGNORED          
                "timezone":   "UTC",                        // time zone of the events, and PT
                "openDate":  "2021-09-12T20:08:00.000Z",    // TO CONVERT IN INTEGER - market open date
                "version":  4029887210,                   // IGNORED A non-monotonically increasing number indicating market changes
                "name":   "Match Odds",                     //
                "eventName":   "Djokovic v Medvedev"        //The name of the event 
              }
            }
            ]
        }
        
        MARKET CHANGE PRICES
        {
          "op":  "mcm",                                     // market change message          
          "clk": "4228566224",                             // sequence number -- IGNORED    
          "pt":  1631486036976,                            // Published Time (in millis since epoch)   
          "mc": [                                                   // Market change Changes to market prices
            {
              "id":   "1.187528277",                        // marketId
            "rc": [                                                 // Runner Change - a list of changes to runners
                {
                  "batl": [                           // batl: best available to lay - LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove). 
                    [ 0, 1.15,50.42],
                    [ 1,1.2,79],
                    [ 2,1.3,43.7]
                  ],
                  "trd": [                                          // Traded PriceVol tuple delta of price changes (0 vol is remove) 
                      [ 1.15, 2.17 ]
                  ],
                  "ltp":  1.01,                            // Last Traded Price - the last price the runner traded at.
                  "tv":  7522103.08,                       // Traded Volume - The total amount matched on the runner 
                "id":  19924831                            // selectionId of the runner
                },
                {
                  "batb": [                              // batb: best available to back - LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove). 
                    [ 0, 3, 9],
                    [ 1, 2.88, 20 ],
                    [ 2,2.14,50 ]
                  ],
                  "batl": [                              // batl: best available to lay - LevelPriceVol triple delta of price changes, keyed by level (0 vol is remove). 
                    [ 0, 200,1 ],
                    [ 1,300, 1],
                    [ 2,500, 1]
                  ],
                  "ltp":  19.0,                             // Last Traded Price - the last price the runner traded at.
                  "tv": 4302965.3,                          // Traded Volume - The total amount matched on the runner 
                  "id":  2249229                            // selectionId of the runner
                }
              ]
            }
          ]
        }

  


