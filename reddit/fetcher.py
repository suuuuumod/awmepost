import requests

from core.fetcher import BaseFetcher
from settings import FETCH_LIMIT, REDDIT_USERNAME


class RedditFetcher(BaseFetcher):
    def fetch(self, subreddit):
        url = f"https://reddit.com/r/{subreddit}/top/.json?limit={FETCH_LIMIT}"
        headers = {
            "User-Agent": f"ChangeMeClient/0.1 by {REDDIT_USERNAME}"
        }
        response = requests.request(method='GET', url=url, headers=headers)
        json = response.json()

        data = []
        if response.status_code == 200:
            data = json['data']['children']
        return data
