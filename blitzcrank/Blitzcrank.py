from blitzcrank.apis.match import Match
from blitzcrank.apis.summoner import Summoner
from blitzcrank.apis.league import League
from blitzcrank.apis.champion_mastery import ChampionMastery
from blitzcrank.apis.champion import Champion
from blitzcrank.apis.item import Item
from blitzcrank.util.session import Session


class Blitzcrank:

    def __init__(self, secret, region):
        self.secret = secret
        self.region = region
        self.extended_region = self._configure_regions(region)

        self.secret = secret
        self.session = Session(secret)

        self._reload_endpoints()
        self.grab = self.Grab()

    def change_rate_limits(self, short_call_limit, short_call_period, long_call_limit, long_call_period):
        self.session = Session(self.secret, short_call_limit, short_call_period, long_call_limit, long_call_period)
        self._reload_endpoints()

    def ignore_rate_limiting(self):
        self.session = Session(self.secret, None, None, None, None)
        self._reload_endpoints()

    def _reload_endpoints(self):
        self.summoner = Summoner(self.region, self.session)
        self.match = Match(self.region, self.session)
        self.league = League(self.region, self.session)
        self.champion_mastery = ChampionMastery(self.region, self.session)
        self.champion = Champion(self.region, self.session)
        self.item = Item(self.region, self.session)

    def _configure_regions(self, region):
        if region in ["euw1", "eun1", "tr1", "ru"]:
            return "europe"
        elif region in ["na1", "br1", "la1", "la2", "oc1"]:
            return "americas"
        elif region in ["kr", "jp1"]:
            return "asia"

    # Grab will contain functions which grab data with limited context, useful for large scale analysis
    # e.g. games on a certain champion, matches in a certain elo, players of a certain elo
    class Grab:
        def games(self, tier=None, champion=None, amount=10):
            pass

        def players(self, tier=None, amount=10):
            pass
