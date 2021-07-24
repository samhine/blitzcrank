import responses
import json
from blitzcrank import Blitzcrank


class TestLeagueEndpoint:

    def test_by_summoner_id(self):
        summoner_id = "fakefakefake"
        region = "euw1"
        expected = {"player": "info"}
        secret = "foo"

        b = Blitzcrank(secret, region)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}',
                     body=json.dumps(expected))

            actual = b.league.by_summoner_id(summoner_id)

            assert actual == expected
            assert rsps.calls[0].request.url == f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
            assert rsps.calls[0].request.headers['X-Riot-Token'] == secret
