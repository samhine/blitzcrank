import requests


class Champion:
    def __init__(self, region: str, session: requests.Session):
        self.region = region
        self.session = session
        self.version = self._request_dd_version()
        self.champion_data = self._request_dd_champion_data()

    def _request_dd_version(self) -> dict:
        return self.session.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

    def _request_dd_champion_data(self) -> dict:
        return self.session.get(f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json")\
                .json()['data']

    def by_id(self, champion_id: str) -> dict:
        return [info for name, info in self.champion_data.items() if info['key'] == str(champion_id)][0]

    def by_name(self, champion_name: str) -> dict:
        return self.champion_data[champion_name]

    def get_all(self) -> list:
        return [name for name in self.champion_data.items()]
