from blitzcrank import Blitzcrank
import json

# Blitzcrank's Match class contains many helper functions to extract information from base match objects.
# These pieces of information may be provided from the Riot API response themselves, or calculated using these base
# data.

b = Blitzcrank("RGAPI-10ec71d4-32b7-464b-a75d-9ce28708f6c7", "euw1")

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
