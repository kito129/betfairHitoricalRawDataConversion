# SUPER IMPORTANT
- [x] ADDITIONAL INFO DONT WORK FOR TENNIS AND FOR SOCCER TOO
# IMPORTANT
- [x] Time alwayas as UTC ms unix timestamp, marketUpdates.openDate must be int in UTC
![img_3.png](img_3.png)  

- [x] if "lengthOddsPrematch" == 0 then  "maxPrematch": null , "minPrematch": null
![img_4.png](img_4.png)
- [x] if "lengthOddsPrematch" == 0 then volumePrematch = 0, add this volume in volumeInplay
- [x] openDate (as all time in the code) must be ms UTC, adn must contain hour minute and sec not only date ( WITH ALL THE ZERO, LIKE THIS 1580580000000)
![img_7.png](img_7.png)

# LAST

- [x] marketUpdate still have complete props
![img_6.png](img_6.png)

- [x] in the final log recap please mark the input and the output to, so I can check how much market are removed or not elaborated

- [x] when save HORSE runners in runnersDB remove the position number if present (ex.     
```json
{
  "id": 27693532,
  "name": "2. Pelonomena",
  "sport": "HORSE RACING"
}, become-->>     
{
  "id": 27693532,
  "name": "Pelonomena",
  "sport": "HORSE RACING"
}, 
```