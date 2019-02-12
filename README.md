# Tomb-of-the-Silken-Thread-Simulator
Simulates going on Expeditions to the "Tomb of the Silken Thread" in [Fallen London](https://www.fallenlondon.com/)
Needs Python Version 3.7


You can use this to check if you should be using "A buccaneering approach" with you current Watchful stat.
To do so just look for the stats section:
```python
# Your stats
# This simulation assumes a minimum watchful of 84 and also having at least 17 supplies at all times during the
# expedition, so we can safely simulate "Other Rivals". It also does not account for stat changes.
watchful = 300
persuasive = 250
use_buccaneering_approach = True
```

input your Watchful and Persuasive and run the script once with
```python
use_buccaneering_approach = True
```
and once with
```python
use_buccaneering_approach = False
```

Higher EPA wins!

#### Update:
According to this script, if your combined watchful is >= 248 you should use "A buccaneering approach"!
