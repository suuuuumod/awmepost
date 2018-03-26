from core.channel import BaseChannel
from core.commands import ActivityCommander, SettingsCommander
from settings import CLEAR_AGE, IMGUR_CHANNEL_ID, MONGO_URI
from .commands import TagsCommander
from .pipes import ImgurPipe
from .settings import ImgurSettings
from .store import ImgurStore


class ImgurChannel(BaseChannel):
    def __init__(self):
        super().__init__()
        self.store = ImgurStore('imgur',
                                url=MONGO_URI,
                                clear_age=CLEAR_AGE)
        self.settings = ImgurSettings(self.store)

        self.commanders = [
            TagsCommander('tags', self.store),
            SettingsCommander('sets', self.settings),
            ActivityCommander('act', self.store),
        ]

    def get_channel_id(self):
        return IMGUR_CHANNEL_ID

    def get_pipes(self):
        return [ImgurPipe()]

    @property
    def commands_handlers(self):
        return [commander.handler for commander in self.commanders]

    def start(self):
        for pipe in self.pipes:
            pipe.set_up(self.channel_id, self.updater, store=self.store, settings=self.settings)
            pipe.start_posting_cycle()

    def help_text(self):
        return '\n'.join([c.get_usage() for c in self.commanders])
