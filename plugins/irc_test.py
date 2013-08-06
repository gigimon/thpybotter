import time
from Queue import Empty

from base import BasePlugin


class IRCPlugin(BasePlugin):
    enabled = False

    def _run(self, msg):
        msg[0].privmsg(msg[1].target, "ok")