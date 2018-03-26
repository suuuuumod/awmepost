from telegram.ext import Updater

from settings import CLEAR_INTERVAL
from core.pipe import BasePipe
from .fetcher import RedditFetcher
from .filters import ScoreFilter, UniqueFilter, NSFWFilter, UniqueUrlFilter
from .modeller import RedditModeller
from .publisher import RedditPublisher
from .store import RedditStore
from .settings import RedditSettings


class RedditPipe(BasePipe):
    modeller_class = RedditModeller

    def __init__(self):
        super().__init__()
        self.store = None
        self.settings = None
        self.limits = []
        self.post_interval = 60

    def set_up(self, channel_id: str, updater: Updater, **kwargs):
        store: RedditStore = kwargs['store']
        settings: RedditSettings = kwargs['settings']
        self.store = store
        self.settings = settings
        super(RedditPipe, self).set_up(channel_id, updater)

    def pre_cycle_hook(self):
        self.post_interval = self.settings.post_interval
        self.scheduler.run_repeating(self.store.clear_ids, interval=CLEAR_INTERVAL, first=0)

    def pre_fetch_hook(self):
        self.set_limits()

    def set_limits(self):
        self.limits = []
        limits = self.store.get()  # { subreddit_name: score_limit }
        for name, score in limits.items():
            self.limits.append((name, score))

    def fetch(self):
        subreddits = []
        fetcher = RedditFetcher()
        for name, score in self.limits:
            subreddits.append(fetcher.fetch(name))
        return subreddits

    def get_pre_filters(self):
        return [UniqueFilter(self.store)]

    def get_post_filters(self):
        return [ScoreFilter(self.limits), UniqueUrlFilter(self.store), NSFWFilter()]

    def get_publisher(self):
        return RedditPublisher(self.channel_id, self.updater, self.store)
