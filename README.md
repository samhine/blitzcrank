# Blitzcrank

[![PyPi](https://img.shields.io/pypi/v/blitzcrank)](https://pypi.org/project/blitzcrank/)
[![Downloads](https://pepy.tech/badge/blitzcrank)](https://pepy.tech/project/blitzcrank)

### Riot API made easy

#### Intoduction

Welcome to Blitzcrank, a module to help with interaction with the Riot API. Although there are many modules like it, most simply act as wrappers to the Riot API without providing much useful functionality. The aim of this project is to make access to the Riot API as painless as possible, while still allowing the richness of data it provides.

While Blitzcrank is easy to use, if you're new to Python or programming in general, take a look at [this guide](https://github.com/samhine/riot-api-demo-python-requests) first and familiarise yourself with Python in general before attempting to use this module. A more well rounded foundation will make it easier for you to grow. This [four hour seminar](https://www.youtube.com/watch?v=rfscVS0vtbw) is suitable for complete programmming beginners.

#### Features
- Built in (custom) rate limiting
- Extra tooling for quick extraction of match data (see `Built in indexing` below)
- Coverage of all base API endpoints the Riot API provides
- Champion/Item APIs to allow built in querying of champion and item IDs, names and statistics

#### Installation

- Install `blitzcrank` using `pip`

    `pip install blitzcrank`

- Import from the same directory level using
    
    `from blitzcrank import Blitzcrank`

#### Getting started

Here's a sample of using Blitzcrank to get base player information;

```
from blitzcrank import Blitzcrank

b = Blitzcrank('RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', 'euw1')
b.summoner.by_name('Montagne')

>> {'id': '5-u_LoLzSaKwdrnG9vK35E8Ju27IXVu6XMM2Y38pxIfhjwM', 
    'accountId': 'igL1_xtGwMyfW89c9EFvok3_yvOGrBOjeosOxL2WtzCg2X4', 
    'puuid': 'k3uFuLaNZplggr93emIb9W3JP0Gf_1D-3vUKt4Bd8m78I1RXiKvvDslyJ53fdbO7zJsN405siJDQPA', 
    'name': 'Montagne', 
    'profileIconId': 691, 
    'revisionDate': 1581790964000, 
    'summonerLevel': 118}
```

For most methods, a summoner name or account ID is needed;

```
from blitzcrank import Blitzcrank

b = Blitzcrank('RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', 'euw1')
s = b.summoner.by_name('Montagne')
b.league.rank_by_summoner_id(s['id'])

>> [{'leagueId': '717ffd55-1b41-4197-bf31-afeafa6346bc', 
    'queueType': 'RANKED_SOLO_5x5', 
    'tier': 'SILVER', 
    'rank': 'I', 
    'summonerId': '5-u_LoLzSaKwdrnG9vK35E8Ju27IXVu6XMM2Y38pxIfhjwM', 
    'summonerName': 'Montagne', 
    'leaguePoints': 39, 
    'wins': 88, 
    'losses': 82, 
    'veteran': True, 
    'inactive': False, 
    'freshBlood': False, 
    'hotStreak': False}]
```

#### Built in indexing

When analysing data, a lot of time is taken making sure you've prefixed correctly according to the [Riot Documentation](https://developer.riotgames.com/apis). Blitzcrank lets you rocket grab statistics in simple one liners. 

```
from blitzcrank import Blitzcrank
import json

b = Blitzcrank("RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", "euw1")

summoner = "Thebausffs"
summoner_id = b.summoner.by_name(summoner).get('accountId')
match_id = b.match.matchlist_by_account(summoner_id, queues=[420])['matches'][0]['gameId']

game_data = b.match.by_id(match_id)
timeline_data = b.match.timeline_by_id(match_id)

stats_array = []

for participant in range(1,11):
    participant_stats = {
        "summoner": b.summoner.by_account(b.match.account_id_for_participant(participant, game_data))["name"],
        "champion": b.match.champion_for_participant(participant, game_data),
        "opposing_champion": b.match.lane_opponent_for_participant(participant, game_data, timeline_data),
        "csdiff@15": b.match.csdiff_at_15_for_participant(participant, game_data, timeline_data),
        "cs_per_min": b.match.cs_per_min_for_participant(participant, game_data),
        "golddiff@15": b.match.golddiff_at_15_for_participant(participant, game_data, timeline_data),
        "gold_per_min": b.match.gold_per_min_for_participant(participant, game_data),
        "control_wards_placed": b.match.control_wards_placed_for_participant(participant, timeline_data)
    }

    stats_array.append(participant_stats)

print(json.dumps(stats_array, sort_keys=True, indent=4))
```

You can find more examples of usage within the [`examples`](https://github.com/samhine/blitzcrank/tree/master/blitzcrank/examples) directory.

##### Note

A lot of the examples utilise `pandas`, a helpful library for dealing with tables of information. Once data is saved within `pandas` into a CSV format, it can be easily copy/pasted into google sheets, or various other locations where scouting reports may be held.

#### Rate limiting
Blitzcrank will by default use the developer API key rate limits. You can change these such as in this example below;
```
from blitzcrank import Blitzcrank

b = Blitzcrank("RGAPI-10ec71d4-32b7-464b-a75d-9ce28708f6c7", "euw1")
b.change_rate_limits(short_call_limit=500, short_call_period=10, =long_call_limit30000, long_call_period=600)
```
There is a more verbose rate limit example in the [`examples`](https://github.com/samhine/blitzcrank/tree/master/blitzcrank/examples) directory, as well as a [test](https://github.com/samhine/blitzcrank/blob/master/blitzcrank/tests/test_rate_limiting.py).

#### Feature request and collaboration

If you'd like to request a feature, please make an issue on this repository with the title starting "FR".
e.g

"FR: Query Riot API for my future"

If you're a developer, and you spot anything that you think can be improved within `blitzcrank`, you are more than welcome to open up a pull request with your desired changes. Any changes which can be well justified, will be implemented.

#### To do's

- Extended documentation of each method (in-line or otherwise)
- Demo video including projects created with Blitzcrank