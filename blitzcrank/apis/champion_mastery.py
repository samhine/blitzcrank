class ChampionMastery:
    def __init__(self, region, session):
        self.region = region
        self.session = session

    def by_summoner_id(self, encrypted_summoner_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encrypted_summoner_id}'
        ).json()

    def by_summoner_id_by_champ_id(self, encrypted_summoner_id: str, champion_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encrypted_summoner_id}/by-champion/{champion_id}'
        ).json()

    def scores_by_summoner_id(self, encrypted_summoner_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{encrypted_summoner_id}'
        ).json()
