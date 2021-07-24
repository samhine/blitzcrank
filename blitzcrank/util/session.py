from ratelimit import limits, sleep_and_retry
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:

    def __init__(self, secret, short_call_limit=20, short_call_period=1, long_call_limit=100, long_call_period=120):
        self.short_call_limit = short_call_limit
        self.short_call_period = short_call_period
        self.long_call_limit = long_call_limit
        self.long_call_period = long_call_period

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=10
        )

        self.http = requests.Session()
        self.http.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        self.http.mount("http://", HTTPAdapter(max_retries=retry_strategy))

        self.headers = {'X-Riot-Token': secret}

        @sleep_and_retry
        @limits(calls=self.short_call_limit, period=self.short_call_period)
        @sleep_and_retry
        @limits(calls=self.long_call_limit, period=self.long_call_period)
        def throttler():
            return

        self.throttler = throttler

    def get(self, url, params=None, **kwargs):
        self.throttler()
        response = self.http.get(url, params=params, headers=self.headers, **kwargs)
        return response
