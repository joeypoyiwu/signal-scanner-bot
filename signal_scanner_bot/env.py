import logging
import os
from threading import Lock
from typing import Optional, Any


log = logging.getLogger(__name__)


_VARS = []


class _State:
    """Class for holding global state across threads/tasks"""

    LISTENING = False
    STOP_REQUESTED = False


def _env(key: str, fail: bool = True, default: Any = None) -> Optional[str]:
    value = os.environ.get(key)
    if value is None:
        if fail and default is None:
            raise KeyError(f"Key '{key}' is not present in environment!")
        return default
    _VARS.append((key, value))
    return value


def log_vars() -> None:
    for key, value in _VARS:
        log.debug(f"{key}={value}")


DEBUG = _env("DEBUG", default=False)
BOT_NUMBER = _env("BOT_NUMBER")
ADMIN_CONTACT = _env("ADMIN_CONTACT")
LISTEN_CONTACT = _env("LISTEN_CONTACT", fail=False)
SIGNAL_TIMEOUT = _env("SIGNAL_TIMEOUT", default=10)
TWITTER_API_KEY = _env("TWITTER_API_KEY")
TWITTER_API_SECRET = _env("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = _env("TWITTER_ACCESS_TOKEN")
TWITTER_TOKEN_SECRET = _env("TWITTER_TOKEN_SECRET")
TRUSTED_TWEETERS = set(str(_env("TRUSTED_TWEETERS", default="")).split(","))

SIGNAL_LOCK = Lock()

STATE = _State()
