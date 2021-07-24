class Summoner:

    def __init__(self, region, session):
        self.region = region
        self.session = session

    # ----------------------- Base API functionality ----------------------- 

    def by_account(self, encrypted_account_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{encrypted_account_id}'
        ).json()

    def by_name(self, summoner_name: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
        ).json()

    def by_puuid(self, encrypted_puuid: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encrypted_puuid}'
        ).json()

    def by_summoner_id(self, encrypted_summoner_id: str) -> dict:
        return self.session.get(
            f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/{encrypted_summoner_id}'
        ).json()

    # ----------------------- Helper functions ----------------------- 

    def get_account_id(self, summoner_name: str) -> str:
        return self.by_name(summoner_name)['accountId']

    def get_level(self, summoner_name: str) -> float:
        return self.by_name(summoner_name)['summonerLevel']

    def get_summoner_id(self, summoner_name: str) -> str:
        return self.by_name(summoner_name)['id']
