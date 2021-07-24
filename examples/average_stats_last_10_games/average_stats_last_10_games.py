from blitzcrank import Blitzcrank
import pandas as pd

# Blitzcrank allows for easy querying of player and game data
# Coupled with pandas, creating performance reports becomes pretty lightweight.

b = Blitzcrank("RGAPI-10ec71d4-32b7-464b-a75d-9ce28708f6c7", "euw1")

columns = ["PLAYER", "CHAMP", "GAMES", "WINS", "GOLDDIFF@15"]
champ_stats = pd.DataFrame(columns=columns)

summoner = "Thebausffs"
summoner_id = b.summoner.by_name(summoner).get('accountId')
matches = b.match.matchlist_by_account(summoner_id, queues=[420])['matches'][:10]

for match in matches:
    match_id = match['gameId']

    game_data = b.match.by_id(match_id)
    timeline_data = b.match.timeline_by_id(match_id)

    participant_id = b.match.participant_id_for_summoner(summoner_id, game_data)

    champ_stats_row = {
        'PLAYER': summoner,
        'CHAMP': b.match.champion_for_participant(participant_id, game_data),
        'GAMES': 1,
        'WINS': 1 if b.match.win_for_participant(participant_id, game_data) else 0,
        'GOLDDIFF@15': float(b.match.golddiff_at_15_for_participant(participant_id, game_data, timeline_data)),
    }

    champ_stats = champ_stats.append(champ_stats_row, ignore_index=True)

aggr = {
    'GAMES': 'sum',
    'WINS': 'sum',
    'GOLDDIFF@15': 'mean'
}

champ_stats_aggr = champ_stats.groupby(['PLAYER', 'CHAMP']).agg(aggr)
champ_stats_sorted = champ_stats_aggr.sort_values(['PLAYER', 'GAMES'], ascending=False)

champ_stats_sorted.to_csv('average_stats_last_10_games_output.csv')
