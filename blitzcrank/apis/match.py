from datetime import datetime
from .champion import Champion
import roleml


class Match:

    def __init__(self, region, extended_region, session):
        self.region = region
        self.extended_region = extended_region
        self.champion = Champion(region, session)
        self.session = session

    # ----------------------- Base API functionality -----------------------

    def by_id(self, match_id: str) -> dict:
        return self.session.get(
            f'https://{self.extended_region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        ).json()

    def matchlist_by_account(self, puuid: str, queue: int = 420, type_: str = "", end_time: int = "",
                             begin_time: int = "", start_index: str = "", count: int = 100) -> dict:
        query_params = {
            "endTime": end_time,
            "beginTime": begin_time,
            "start": start_index,
            "count": count,
            "queue": queue,
            "type": type_,
        }
        return self.session.get(
            f'https://{self.extended_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?'
            + ''.join([k + "=" + str(v) + "&" for k, v in query_params.items() if v])
        ).json()

    def timeline_by_id(self, match_id: str) -> str:
        return self.session.get(
            f'https://{self.extended_region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline'
        ).json()

    # ----------------------- Helper functions -----------------------

    def is_champ_in_game(self, champion_id, match_data):
        for participant in match_data['info']['participants']:
            if str(participant['championId']) == str(champion_id):
                return True
        return False

    def get_combined_game_info(self, match_id):
        return {
            "match": self.by_id(match_id),
            "timeline": self.timeline_by_id(match_id)
        }

    # NB: Will not work on custom game data since identities of participants is hidden
    def puuid_for_participant(self, participant_id, match_data):
        account_id = [player["player"]['currentAccountId'] for player in match_data["participants"] if
                      player["participantId"] == participant_id][0]
        return account_id

    # NB: Will not work on custom game data since identities of participants is hidden
    def participant_id_for_summoner(self, puuid, match_data):
        part_id = [player['participantId'] for player in match_data["participants"] if
                   player["puuid"] == puuid][0]
        return part_id

    def summoner_for_participant(self, participant_id, match_data):
        summoner_name = [player["summonerName"] for player in match_data["participants"] if
                         player["participantId"] == participant_id][0]
        return summoner_name

    def side_for_participant(self, participant_id, match_data):
        side = [info for info in match_data["participants"] if info['participantId'] == participant_id][0]['teamId']
        return "blue" if side == 100 else "red"

    def games_for_day(self, day, puuid):
        matches = self.matchlist_by_account(
            puuid,
            queue=420,
            begin_time=int(datetime.strptime(day, '%Y-%m-%d').timestamp()) * 1000,
            end_time=(int(datetime.strptime(day, '%Y-%m-%d').timestamp()) + 86400) * 1000)
        try:
            return matches['matches']
        except KeyError:
            return []

    def kills_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['kills']

    def deaths_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['deaths']

    def assists_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['assists']

    def kpp_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]

        if int(participant_id) <= 5:
            total_team_kills = sum([self.kills_for_participant(id, match_data) for id in range(1, 6)])
        else:
            total_team_kills = sum([self.kills_for_participant(id, match_data) for id in range(6, 11)])

        if not total_team_kills:
            return 0
        return ((participant_info['kills'] + participant_info['assists']) / total_team_kills) * 100

    def dmg_to_champs_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['totalDamageDealtToChampions']

    def tot_dmg_to_champs_per_min_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['totalDamageDealtToChampions'] / (match_data['gameDuration'] / 60)

    def gold_per_min_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        participant_stats = participant_info['stats']
        return participant_stats['goldEarned'] / (match_data['gameDuration'] / 60)

    def vision_score_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['visionScore']

    def kdr_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        deaths = participant_info['deaths']
        if not deaths: deaths = 1
        return (participant_info['kills'] + participant_info['assists']) / deaths

    def kda_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return str(participant_info['kills']) + "/" + str(participant_info['deaths']) + "/" + str(
            participant_info['assists'])

    def win_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        return participant_info['win']

    def csdiff_at_10_for_participant(self, participant_id, match_data, timeline_data):
        minute_10_frames = timeline_data['frames'][10]['participantFrames']
        participant_info = \
            [info for key, info in minute_10_frames.items() if info['participantId'] == int(participant_id)][0]

        roles = roleml.predict(match_data, timeline_data)
        participant_role = roles[int(participant_id)]
        opponent_participant_id = \
            [id for id, role in roles.items() if role == participant_role and id != int(participant_id)][0]

        opponent_participant_info = \
            [info for key, info in minute_10_frames.items() if info['participantId'] == int(opponent_participant_id)][0]

        return participant_info['minionsKilled'] - opponent_participant_info['minionsKilled']

    def xpdiff_at_10_for_participant(self, participant_id, match_data, timeline_data):
        minute_10_frames = timeline_data['frames'][10]['participantFrames']
        participant_info = \
            [info for key, info in minute_10_frames.items() if info['participantId'] == int(participant_id)][0]

        roles = roleml.predict(match_data, timeline_data)
        participant_role = roles[int(participant_id)]
        opponent_participant_id = \
            [id for id, role in roles.items() if role == participant_role and id != int(participant_id)][0]

        opponent_participant_info = \
            [info for key, info in minute_10_frames.items() if info['participantId'] == int(opponent_participant_id)][0]

        return participant_info['xp'] - opponent_participant_info['xp']

    def control_wards_purchased_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        control_wards_purchased = participant_info['visionWardsBoughtInGame']
        return float(control_wards_purchased)

    def wards_placed_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        wards_placed = participant_info['wardsPlaced']
        return float(wards_placed)

    def wards_destroyed_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        wards_destroyed = participant_info['wardsKilled']
        return float(wards_destroyed)

    def control_wards_placed_for_participant(self, participant_id, timeline_data):
        frames = timeline_data['frames']

        wards = 0
        for frame in frames:
            if frame.get('events'):
                wards += len([event for event in frame['events']
                              if event['type'] == 'WARD_PLACED'
                              and event['creatorId'] == int(participant_id)
                              and event["wardType"] == "CONTROL_WARD"
                              ])

        return wards

    def solo_kills_for_participant(self, participant_id, timeline_data):
        frames = timeline_data['frames']
        count = 0
        for frame in frames:
            if frame.get('events'):
                solo_kills_maybe = [event for event in frame['events']
                                    if event['type'] == 'CHAMPION_KILL'
                                    and event['killerId'] == int(participant_id)
                                    and event['assistingParticipantIds'] == []
                                    ]
                # print(solo_kills_maybe)
                count += len(solo_kills_maybe)
        return count

    def solo_deaths_for_participant(self, participant_id, timeline_data):
        frames = timeline_data['frames']
        count = 0
        for frame in frames:
            if frame.get('events'):
                solo_deaths_maybe = [event for event in frame['events']
                                     if event['type'] == 'CHAMPION_KILL'
                                     and event['victimId'] == int(participant_id)
                                     and event['assistingParticipantIds'] == []
                                     ]
                # print(solo_kills_maybe)
                count += len(solo_deaths_maybe)
        return count

    def trinket_switch_time_for_participant(self, participant_id, timeline_data):
        frames = timeline_data['frames']
        timestamp = 0
        for frame in frames:
            if frame.get('events'):
                timestamp_maybe = [event for event in frame['events']
                                   if event['type'] == 'ITEM_PURCHASED'
                                   and (event['itemId'] == 3364 or event['itemId'] == 3187)
                                   and event["participantId"] == int(participant_id)
                                   ]
                if timestamp_maybe:
                    timestamp = timestamp_maybe[0]["timestamp"]
        return timestamp / 60000

    def death_total_for_participant_team(self, participant_id, match_data):
        if int(participant_id) <= 5:
            total_team_deaths = sum([info['deaths']
                                     for info in match_data['info']['participants'] if int(info['participantId']) <= 5])
        else:
            total_team_deaths = sum([info['deaths']
                                     for info in match_data['info']['participants'] if int(info['participantId']) >= 5])
        return total_team_deaths

    def kill_total_for_participant_team(self, participant_id, match_data):
        if int(participant_id) <= 5:
            total_team_kills = sum([info['kills']
                                    for info in match_data['info']['participants'] if int(info['participantId']) <= 5])
        else:
            total_team_kills = sum([info['kills']
                                    for info in match_data['info']['participants'] if int(info['participantId']) >= 5])
        return total_team_kills

    def dmg_total_for_participant_team(self, participant_id, match_data):
        if int(participant_id) <= 5:
            total_team_dmg = sum([info['totalDamageDealtToChampions']
                                  for info in match_data['info']['participants'] if int(info['participantId']) <= 5])
        else:
            total_team_dmg = sum([info['totalDamageDealtToChampions']
                                  for info in match_data['info']['participants'] if int(info['participantId']) >= 5])
        return total_team_dmg

    def dmg_percent_for_participant(self, participant_id, match_data):
        total_team_dmg = self.dmg_total_for_participant_team(participant_id, match_data)
        participant_dmg = self.dmg_to_champs_for_participant(participant_id, match_data)
        return (participant_dmg / total_team_dmg) * 100

    def cs_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        total_cs_killed = participant_info['totalMinionsKilled']
        return total_cs_killed

    def cs_per_min_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        total_cs_killed = participant_info['totalMinionsKilled']
        game_length_in_minutes = match_data['gameDuration'] / 60

        return total_cs_killed / game_length_in_minutes

    def champion_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        champion_id = participant_info['championId']
        champion_name = self.champion.by_id(champion_id).get('name')

        return champion_name

    def role_for_participant(self, participant_id, match_data):
        participant_info = [info for info in match_data['info']['participants'] if info['participantId'] == participant_id][0]
        participant_role = participant_info['individualPosition']
        return participant_role

    def lane_opponent_for_participant(self, participant_id, match_data, timeline_data):

        participant_role = self.role_for_participant(participant_id)
        opponent_participant_id = [info['participantId'] for info in match_data['info']['participants']
                                   if participant_role == info['individualPosition']
                                   and participant_id != info['participantId']]
        opponent_info = \
            [info for info in match_data['info']['participants'] if info['participantId'] == opponent_participant_id][0]
        champion_id = opponent_info['championId']
        champion_name = self.champion.by_id(champion_id).get('name')
        return champion_name

    def deaths_at_15_for_participant(self, participant_id, timeline_data):
        frames_of_interest = timeline_data['frames'][:16]

        deaths = 0
        for frame in frames_of_interest:
            if frame.get('events'):
                deaths += len([event for event in frame['events'] if
                               event['type'] == 'CHAMPION_KILL' and event['victimId'] == int(participant_id)])

        return deaths

    def csdiff_at_15_for_participant(self, participant_id, match_data, timeline_data):
        minute_15_frames = timeline_data['frames'][15]['participantFrames']
        participant_info = \
            [info for key, info in minute_15_frames.items() if info['participantId'] == int(participant_id)][0]

        roles = roleml.predict(match_data, timeline_data)
        participant_role = roles[int(participant_id)]
        opponent_participant_id = \
            [id for id, role in roles.items() if role == participant_role and id != int(participant_id)][0]

        opponent_participant_info = \
            [info for key, info in minute_15_frames.items() if info['participantId'] == int(opponent_participant_id)][0]

        return participant_info['minionsKilled'] - opponent_participant_info['minionsKilled']

    def xpdiff_at_15_for_participant(self, participant_id, match_data, timeline_data):
        minute_15_frames = timeline_data['frames'][15]['participantFrames']
        participant_info = \
            [info for key, info in minute_15_frames.items() if info['participantId'] == int(participant_id)][0]

        roles = roleml.predict(match_data, timeline_data)
        participant_role = roles[int(participant_id)]
        opponent_participant_id = \
            [id for id, role in roles.items() if role == participant_role and id != int(participant_id)][0]

        opponent_participant_info = \
            [info for key, info in minute_15_frames.items() if info['participantId'] == int(opponent_participant_id)][0]

        return participant_info['xp'] - opponent_participant_info['xp']

    def golddiff_at_10_for_participant(self, participant_id, match_data, timeline_data):
        minute_10_frames = timeline_data['frames'][15]['participantFrames']
        participant_info = \
            [info for key, info in minute_10_frames.items() if info['participantId'] == int(participant_id)][0]

        roles = roleml.predict(match_data, timeline_data)
        participant_role = roles[int(participant_id)]
        opponent_participant_id = \
            [id for id, role in roles.items() if role == participant_role and id != int(participant_id)][0]

        opponent_participant_info = \
            [info for key, info in minute_10_frames.items() if info['participantId'] == int(opponent_participant_id)][0]

        return participant_info['totalGold'] - opponent_participant_info['totalGold']

    def golddiff_at_15_for_participant(self, participant_id, match_data, timeline_data):
        minute_15_frames = timeline_data['frames'][15]['participantFrames']
        participant_info = \
            [info for key, info in minute_15_frames.items() if info['participantId'] == int(participant_id)][0]

        roles = roleml.predict(match_data, timeline_data)
        participant_role = roles[int(participant_id)]
        opponent_participant_id = \
            [id for id, role in roles.items() if role == participant_role and id != int(participant_id)][0]

        opponent_participant_info = \
            [info for key, info in minute_15_frames.items() if info['participantId'] == int(opponent_participant_id)][0]

        return participant_info['totalGold'] - opponent_participant_info['totalGold']

    def first_blood_for_side(self, side, match_data):
        side_info = [info for info in match_data['info']['participants']
                     if info['firstBloodKill']
                     and info['teamId'] == side][0]
        return side_info['firstBlood']

    def first_turret_for_side(self, side, match_data):
        side_info = [info['objectives'] for info in match_data['teams'] if info['teamId'] == side][0]
        return side_info['tower']['first']

    def heralds_for_side(self, side, match_data):
        side_info = [info['objectives'] for info in match_data['teams'] if info['teamId'] == side][0]
        return side_info['riftHerald']['kills']

    def barons_for_side(self, side, match_data):
        side_info = [info['objectives'] for info in match_data['teams'] if info['teamId'] == side][0]
        return side_info['baron']['kills']

    def dragons_for_side(self, side, match_data):
        side_info = [info['objectives'] for info in match_data['teams'] if info['teamId'] == side][0]
        return side_info['dragon']['kills']
