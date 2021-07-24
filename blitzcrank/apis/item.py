class Item:
    def __init__(self, region, session):
        self.region = region
        self.session = session
        self.version = self._request_dd_version()
        self.item_data = self._request_dd_item_data()

    def _request_dd_version(self) -> str:
        return self.session.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

    def _request_dd_item_data(self) -> dict:
        return self.session.get(f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/item.json")\
                .json()['data']
    
    def by_id(self, item_id: str) -> dict:
        return self.item_data[item_id]

    def by_name(self, item_name: str) -> dict:
        return [info for name, info in self.item_data.items() if info['name'] == str(item_name)][0]

    def get_all(self) -> list:
        return [name for name in self.item_data.items()]