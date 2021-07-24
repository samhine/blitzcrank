from blitzcrank import Blitzcrank

b = Blitzcrank("RGAPI-9f5eb028-01bc-4805-a297-240f22e3455a","euw1")

# Extract from URL;
# https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT05/1822216?gameHash=909ab1b1f41b1e48&tab=overview
match = ["ESPORTSTMNT05","1822216","909ab1b1f41b1e48","blue"]

# You must first look at the ACS match history page, and copy/paste your cookie information here to validate requests
# Docs - https://www.hextechdocs.dev/lol/esportsapi/13.esports-match-data#in-need-of-cookies
cookies = ""

platform = match[0]
game_id = match[1]
game_hash = match[2]

match_data = b.match.by_id_official(game_id, platform, game_hash, cookies)
timeline_data = b.match.timeline_by_id_official(game_id, platform, game_hash, cookies)

chosen_participant = 1
print(b.match.solo_kills_for_participant(chosen_participant, timeline_data))