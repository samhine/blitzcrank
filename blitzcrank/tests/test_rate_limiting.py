from blitzcrank import Blitzcrank
import responses
import json


class TestRateLimiting:

    def test_default_rate_limits(self):
        secret = "fakefakefake"
        region = "euw1"
        summoner_name = "foo"
        api_rsp = {'accountId': '123'}

        b = Blitzcrank(secret, region)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}',
                     body=json.dumps(api_rsp))

            for c in range(100):
                b.summoner.get_account_id(summoner_name)

            assert len(rsps.calls) == 100   # No failure even though we have exceeded the default rate limits
