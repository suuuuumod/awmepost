from functools import wraps
from telegram import Bot, Update


def admin_access(admins_list=None):
    def access(func):
        @wraps(func)
        def wrapped(self, bot: Bot, update: Update, *args, **kwargs):
            user = update.effective_user
            admins = None
            if admins_list is None:
                admins = getattr(self, 'admins', None)

            if admins is None:
                return func(self, bot, update, *args, **kwargs)


            return func(self, bot, update, *args, **kwargs)
        return wrapped
    return access


def log(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return wrapper


def mega_log(print_res=False, print_end=False):
    def decorator(func):

        @wraps(func)
        def wrapped(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            return result

        return wrapped
    return decorator
