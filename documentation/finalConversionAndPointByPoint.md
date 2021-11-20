
   COMPLETE DATA - V2 // TENNIS POINT HAVE TIME STAMP
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
                "winnerPoint": 9980                    // columns N
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
            },
            "pointByPoint": {                                       // we have to convert this data in JSON and save
                <event id="766912349" type="first_serve" time="2020-10-19T08:18:08+00:00" competitor="away"/>

                <event id="766913905" type="match_started" time="2020-10-19T08:23:02+00:00"/>

                <event id="766913907" type="period_start" time="2020-10-19T08:23:02+00:00" period_name="1st_set"/>

                <event id="766913993" type="point" time="2020-10-19T08:23:15+00:00" competitor="home"
                home_score="15" away_score="0" server="away" result="receiver_won"/>

                <event id="766914171" type="point" time="2020-10-19T08:23:49+00:00" competitor="home"
                home_score="30" away_score="0" server="away" result="double_fault" first_serve_fault="true"/>

                <event id="766914351" type="point" time="2020-10-19T08:24:23+00:00" competitor="home"
                home_score="40" away_score="0" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766914469" type="point" time="2020-10-19T08:24:48+00:00" competitor="away"
                home_score="40" away_score="15" server="away" result="server_won"/>

                <event id="766914681" type="point" time="2020-10-19T08:25:28+00:00" competitor="away"
                home_score="40" away_score="30" server="away" result="server_won"/>

                <event id="766914829" type="point" time="2020-10-19T08:25:53+00:00" competitor="away"
                home_score="40" away_score="40" server="away" result="server_won"/>

                <event id="766915055" type="point" time="2020-10-19T08:26:30+00:00" competitor="home"
                home_score="50" away_score="40" server="away" result="receiver_won"/>

                <event id="766915297" type="period_score" time="2020-10-19T08:27:25+00:00" period="1"
                home_score="1" away_score="0" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766915653" type="point" time="2020-10-19T08:28:31+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="server_won"/>

                <event id="766915815" type="point" time="2020-10-19T08:29:02+00:00" competitor="home"
                home_score="30" away_score="0" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766915929" type="point" time="2020-10-19T08:29:29+00:00" competitor="away"
                home_score="30" away_score="15" server="home" result="receiver_won"/>

                <event id="766916087" type="point" time="2020-10-19T08:29:59+00:00" competitor="away"
                home_score="30" away_score="30" server="home" result="receiver_won"/>

                <event id="766916219" type="point" time="2020-10-19T08:30:27+00:00" competitor="home"
                home_score="40" away_score="30" server="home" result="server_won"/>

                <event id="766916343" type="period_score" time="2020-10-19T08:30:43+00:00" period="1"
                home_score="2" away_score="0" server="home" result="server_won"/>

                <event id="766916661" type="point" time="2020-10-19T08:31:39+00:00" competitor="away"
                home_score="0" away_score="15" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766916821" type="point" time="2020-10-19T08:32:06+00:00" competitor="home"
                home_score="15" away_score="15" server="away" result="receiver_won"/>

                <event id="766916937" type="point" time="2020-10-19T08:32:27+00:00" competitor="away"
                home_score="15" away_score="30" server="away" result="server_won"/>

                <event id="766917163" type="point" time="2020-10-19T08:33:04+00:00" competitor="home"
                home_score="30" away_score="30" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766917415" type="point" time="2020-10-19T08:33:53+00:00" competitor="home"
                home_score="40" away_score="30" server="away" result="receiver_won"/>

                <event id="766917523" type="point" time="2020-10-19T08:34:18+00:00" competitor="away"
                home_score="40" away_score="40" server="away" result="server_won"/>

                <event id="766917611" type="point" time="2020-10-19T08:34:39+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won"/>

                <event id="766917803" type="period_score" time="2020-10-19T08:35:22+00:00" period="1"
                home_score="2" away_score="1" server="away" result="server_won"/>

                <event id="766918303" type="point" time="2020-10-19T08:37:10+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="server_won"/>

                <event id="766918447" type="point" time="2020-10-19T08:37:34+00:00" competitor="home"
                home_score="30" away_score="0" server="home" result="server_won"/>

                <event id="766918549" type="point" time="2020-10-19T08:37:53+00:00" competitor="home"
                home_score="40" away_score="0" server="home" result="ace"/>

                <event id="766918721" type="period_score" time="2020-10-19T08:38:29+00:00" period="1"
                home_score="3" away_score="1" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766919137" type="point" time="2020-10-19T08:39:35+00:00" competitor="home"
                home_score="15" away_score="0" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766919323" type="point" time="2020-10-19T08:40:10+00:00" competitor="away"
                home_score="15" away_score="15" server="away" result="server_won"/>

                <event id="766919553" type="point" time="2020-10-19T08:40:43+00:00" competitor="home"
                home_score="30" away_score="15" server="away" result="receiver_won"/>

                <event id="766919815" type="point" time="2020-10-19T08:41:21+00:00" competitor="home"
                home_score="40" away_score="15" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766919925" type="period_score" time="2020-10-19T08:41:45+00:00" period="1"
                home_score="4" away_score="1" server="away" result="receiver_won"/>

                <event id="766920329" type="point" time="2020-10-19T08:43:25+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="server_won"/>

                <event id="766920431" type="point" time="2020-10-19T08:43:50+00:00" competitor="home"
                home_score="30" away_score="0" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766920535" type="point" time="2020-10-19T08:44:11+00:00" competitor="home"
                home_score="40" away_score="0" server="home" result="server_won"/>

                <event id="766920661" type="period_score" time="2020-10-19T08:44:36+00:00" period="1"
                home_score="5" away_score="1" server="home" result="server_won"/>

                <event id="766921059" type="point" time="2020-10-19T08:45:51+00:00" competitor="away"
                home_score="0" away_score="15" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766921239" type="point" time="2020-10-19T08:46:24+00:00" competitor="home"
                home_score="15" away_score="15" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766921329" type="point" time="2020-10-19T08:46:44+00:00" competitor="home"
                home_score="30" away_score="15" server="away" result="receiver_won"/>

                <event id="766921495" type="point" time="2020-10-19T08:47:18+00:00" competitor="home"
                home_score="40" away_score="15" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766921663" type="point" time="2020-10-19T08:47:52+00:00" competitor="away"
                home_score="40" away_score="30" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766921789" type="point" time="2020-10-19T08:48:22+00:00" competitor="away"
                home_score="40" away_score="40" server="away" result="server_won"/>

                <event id="766921891" type="point" time="2020-10-19T08:48:44+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won"/>

                <event id="766922043" type="point" time="2020-10-19T08:49:24+00:00" competitor="home"
                home_score="40" away_score="40" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766922283" type="point" time="2020-10-19T08:50:13+00:00" competitor="home"
                home_score="50" away_score="40" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766922655" type="point" time="2020-10-19T08:51:17+00:00" competitor="away"
                home_score="40" away_score="40" server="away" result="server_won"/>

                <event id="766923489" type="point" time="2020-10-19T08:53:47+00:00" competitor="home"
                home_score="50" away_score="40" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766923725" type="point" time="2020-10-19T08:54:34+00:00" competitor="away"
                home_score="40" away_score="40" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766923879" type="point" time="2020-10-19T08:55:07+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766924067" type="point" time="2020-10-19T08:55:41+00:00" competitor="home"
                home_score="40" away_score="40" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766924307" type="point" time="2020-10-19T08:56:38+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766924505" type="point" time="2020-10-19T08:57:23+00:00" competitor="home"
                home_score="40" away_score="40" server="away" result="receiver_won"/>

                <event id="766924637" type="point" time="2020-10-19T08:57:50+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won"/>

                <event id="766924887" type="point" time="2020-10-19T08:58:31+00:00" competitor="home"
                home_score="40" away_score="40" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766925129" type="point" time="2020-10-19T08:59:23+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766925333" type="period_score" time="2020-10-19T09:00:03+00:00" period="1"
                home_score="5" away_score="2" server="away" result="server_won"/>

                <event id="766926361" type="point" time="2020-10-19T09:02:11+00:00" competitor="away"
                home_score="0" away_score="15" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766926531" type="point" time="2020-10-19T09:02:41+00:00" competitor="home"
                home_score="15" away_score="15" server="home" result="server_won"/>

                <event id="766926779" type="point" time="2020-10-19T09:03:17+00:00" competitor="home"
                home_score="30" away_score="15" server="home" result="server_won"/>

                <event id="766926975" type="point" time="2020-10-19T09:03:48+00:00" competitor="home"
                home_score="40" away_score="15" server="home" result="server_won"/>

                <event id="766927175" type="point" time="2020-10-19T09:04:17+00:00" competitor="away"
                home_score="40" away_score="30" server="home" result="receiver_won"/>

                <event id="766927307" type="period_score" time="2020-10-19T09:04:44+00:00" period="1"
                home_score="6" away_score="2" server="home" result="server_won"/>

                <event id="766927311" type="period_start" time="2020-10-19T09:04:44+00:00"
                period_name="2nd_set"/>

                <event id="766928465" type="point" time="2020-10-19T09:07:30+00:00" competitor="home"
                home_score="15" away_score="0" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766928725" type="point" time="2020-10-19T09:08:09+00:00" competitor="home"
                home_score="30" away_score="0" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766928981" type="point" time="2020-10-19T09:08:40+00:00" competitor="home"
                home_score="40" away_score="0" server="away" result="receiver_won"/>

                <event id="766929121" type="point" time="2020-10-19T09:09:03+00:00" competitor="away"
                home_score="40" away_score="15" server="away" result="server_won"/>

                <event id="766929215" type="point" time="2020-10-19T09:09:23+00:00" competitor="away"
                home_score="40" away_score="30" server="away" result="server_won"/>

                <event id="766929353" type="point" time="2020-10-19T09:09:46+00:00" competitor="away"
                home_score="40" away_score="40" server="away" result="server_won"/>

                <event id="766929527" type="point" time="2020-10-19T09:10:11+00:00" competitor="away"
                home_score="40" away_score="50" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766929757" type="period_score" time="2020-10-19T09:10:44+00:00" period="2"
                home_score="0" away_score="1" server="away" result="server_won"/>

                <event id="766930235" type="point" time="2020-10-19T09:12:08+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766930477" type="point" time="2020-10-19T09:12:43+00:00" competitor="away"
                home_score="15" away_score="15" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766930631" type="point" time="2020-10-19T09:13:07+00:00" competitor="away"
                home_score="15" away_score="30" server="home" result="receiver_won"/>

                <event id="766930949" type="point" time="2020-10-19T09:13:50+00:00" competitor="away"
                home_score="15" away_score="40" server="home" result="receiver_won"/>

                <event id="766931095" type="point" time="2020-10-19T09:14:15+00:00" competitor="home"
                home_score="30" away_score="40" server="home" result="server_won"/>

                <event id="766931291" type="point" time="2020-10-19T09:14:44+00:00" competitor="home"
                home_score="40" away_score="40" server="home" result="server_won"/>

                <event id="766931411" type="point" time="2020-10-19T09:15:10+00:00" competitor="home"
                home_score="50" away_score="40" server="home" result="server_won"/>

                <event id="766931587" type="period_score" time="2020-10-19T09:15:36+00:00" period="2"
                home_score="1" away_score="1" server="home" result="server_won"/>

                <event id="766932001" type="point" time="2020-10-19T09:16:16+00:00" competitor="away"
                home_score="0" away_score="15" server="away" result="server_won"/>

                <event id="766932101" type="point" time="2020-10-19T09:16:28+00:00" competitor="home"
                home_score="15" away_score="15" server="away" result="receiver_won"/>

                <event id="766932413" type="point" time="2020-10-19T09:17:11+00:00" competitor="home"
                home_score="30" away_score="15" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766932635" type="point" time="2020-10-19T09:17:51+00:00" competitor="home"
                home_score="40" away_score="15" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766932867" type="point" time="2020-10-19T09:18:30+00:00" competitor="away"
                home_score="40" away_score="30" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766933059" type="period_score" time="2020-10-19T09:19:04+00:00" period="2"
                home_score="2" away_score="1" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766933853" type="point" time="2020-10-19T09:21:14+00:00" competitor="away"
                home_score="0" away_score="15" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766934079" type="point" time="2020-10-19T09:21:51+00:00" competitor="away"
                home_score="0" away_score="30" server="home" result="receiver_won"/>

                <event id="766934371" type="point" time="2020-10-19T09:22:32+00:00" competitor="home"
                home_score="15" away_score="30" server="home" result="server_won"/>

                <event id="766934563" type="point" time="2020-10-19T09:23:03+00:00" competitor="home"
                home_score="30" away_score="30" server="home" result="server_won"/>

                <event id="766934683" type="point" time="2020-10-19T09:23:21+00:00" competitor="home"
                home_score="40" away_score="30" server="home" result="server_won"/>

                <event id="766934937" type="period_score" time="2020-10-19T09:24:06+00:00" period="2"
                home_score="3" away_score="1" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766935117" type="point" time="2020-10-19T09:24:48+00:00" competitor="away"
                home_score="0" away_score="15" server="away" result="server_won"/>

                <event id="766935243" type="point" time="2020-10-19T09:25:09+00:00" competitor="away"
                home_score="0" away_score="30" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766935379" type="point" time="2020-10-19T09:25:32+00:00" competitor="home"
                home_score="15" away_score="30" server="away" result="receiver_won"/>

                <event id="766935581" type="point" time="2020-10-19T09:26:09+00:00" competitor="away"
                home_score="15" away_score="40" server="away" result="server_won" first_serve_fault="true"/>

                <event id="766935789" type="point" time="2020-10-19T09:26:43+00:00" competitor="home"
                home_score="30" away_score="40" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766935961" type="period_score" time="2020-10-19T09:27:15+00:00" period="2"
                home_score="3" away_score="2" server="away" result="server_won"/>

                <event id="766936657" type="point" time="2020-10-19T09:29:16+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="ace"/>

                <event id="766937409" type="point" time="2020-10-19T09:31:33+00:00" competitor="away"
                home_score="15" away_score="15" server="home" result="receiver_won"/>

                <event id="766937419" type="point" time="2020-10-19T09:31:35+00:00" competitor="home"
                home_score="30" away_score="15" server="home" result="server_won"/>

                <event id="766937421" type="point" time="2020-10-19T09:31:36+00:00" competitor="home"
                home_score="40" away_score="15" server="home" result="server_won"/>

                <event id="766937523" type="point" time="2020-10-19T09:31:53+00:00" competitor="away"
                home_score="40" away_score="30" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766937685" type="period_score" time="2020-10-19T09:32:29+00:00" period="2"
                home_score="4" away_score="2" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766938077" type="point" time="2020-10-19T09:33:26+00:00" competitor="home"
                home_score="15" away_score="0" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766938235" type="point" time="2020-10-19T09:33:50+00:00" competitor="home"
                home_score="30" away_score="0" server="away" result="receiver_won"/>

                <event id="766938393" type="point" time="2020-10-19T09:34:18+00:00" competitor="home"
                home_score="40" away_score="0" server="away" result="receiver_won"/>

                <event id="766938569" type="period_score" time="2020-10-19T09:34:50+00:00" period="2"
                home_score="5" away_score="2" server="away" result="receiver_won" first_serve_fault="true"/>

                <event id="766939389" type="point" time="2020-10-19T09:36:38+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766939537" type="point" time="2020-10-19T09:37:09+00:00" competitor="away"
                home_score="15" away_score="15" server="home" result="receiver_won"/>

                <event id="766939701" type="point" time="2020-10-19T09:37:33+00:00" competitor="home"
                home_score="30" away_score="15" server="home" result="server_won"/>

                <event id="766939935" type="point" time="2020-10-19T09:38:13+00:00" competitor="away"
                home_score="30" away_score="30" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766940151" type="point" time="2020-10-19T09:38:50+00:00" competitor="away"
                home_score="30" away_score="40" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766940495" type="period_score" time="2020-10-19T09:39:55+00:00" period="2"
                home_score="5" away_score="3" server="home" result="receiver_won" first_serve_fault="true"/>

                <event id="766940835" type="point" time="2020-10-19T09:40:50+00:00" competitor="away"
                home_score="0" away_score="15" server="away" result="server_won"/>

                <event id="766940899" type="point" time="2020-10-19T09:41:03+00:00" competitor="away"
                home_score="0" away_score="30" server="away" result="server_won"/>

                <event id="766941015" type="point" time="2020-10-19T09:41:17+00:00" competitor="away"
                home_score="0" away_score="40" server="away" result="server_won"/>

                <event id="766941125" type="point" time="2020-10-19T09:41:33+00:00" competitor="home"
                home_score="15" away_score="40" server="away" result="receiver_won"/>

                <event id="766941253" type="period_score" time="2020-10-19T09:41:56+00:00" period="2"
                home_score="5" away_score="4" server="away" result="ace"/>

                <event id="766941903" type="point" time="2020-10-19T09:43:48+00:00" competitor="home"
                home_score="15" away_score="0" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766942129" type="point" time="2020-10-19T09:44:28+00:00" competitor="home"
                home_score="30" away_score="0" server="home" result="server_won" first_serve_fault="true"/>

                <event id="766942245" type="point" time="2020-10-19T09:44:52+00:00" competitor="home"
                home_score="40" away_score="0" server="home" result="server_won"/>

                <event id="766942341" type="period_score" time="2020-10-19T09:45:11+00:00" period="2"
                home_score="6" away_score="4" server="home" result="server_won"/>

                <event id="766942345" type="match_ended" time="2020-10-19T09:45:11+00:00"/>
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

