import responses
import json
from blitzcrank import Blitzcrank


class TestSummonerEndpoint:

    def test_helper_functions(self):
        summoner_name = "fakefakefake"
        api_rsp = {'accountId': '123', 'summonerLevel': 23, 'id': '234'}
        region = "euw1"
        secret = "foo"

        b = Blitzcrank(secret, region)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}',
                     body=json.dumps(api_rsp))

            actual_account_id = b.summoner.get_account_id(summoner_name)
            actual_level = b.summoner.get_level(summoner_name)
            actual_summoner_id = b.summoner.get_summoner_id(summoner_name)

            assert actual_account_id == api_rsp['accountId']
            assert actual_level == api_rsp['summonerLevel']
            assert actual_summoner_id == api_rsp['id']
            assert len(rsps.calls) == 3
            assert rsps.calls[0].request.headers['X-Riot-Token'] == secret
