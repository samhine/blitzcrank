class League:
    def __init__(self, region, session):
        self.region = region
        self.session = session

    # ----------------------- Base API functionality -----------------------
    def by_summoner_id(self, encrypted_summoner_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_summoner_id}'
        ).json()

    def by_id(self, league_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/league/v4/leagues/{league_id}'
        ).json()

    def challenger_leagues_by_queue(self, queue: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}'
        ).json()

    def grandmaster_leagues_by_queue(self, queue: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}'
        ).json()

    def master_leagues_by_queue(self, queue: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}'
        ).json()

        # ----------------------- Helper functions -----------------------

    def rank_by_summoner_id(self, encrypted_summoner_id: str) -> dict:
        d = self.by_summoner_id(encrypted_summoner_id)
        if d:
            rank_info = {
                "tier": d['tier'],
                "rank": d['rank'],
                "lp": d['leaguePoints']
            }
        else:
            rank_info = {
                "tier": "UNRANKED",
                "rank": "IV",
                "lp": 0
            }
        return rank_info
