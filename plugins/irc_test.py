import time
from Queue import Empty

from base import BasePlugin


class IRCPlugin(BasePlugin):
    enabled = False

    def run(self):
        while True:
            try:
                msg = self._queue.get(timeout=15)
            except Empty:
                time.sleep(1)
                continue
            print "Get message from %s" % msg[1].arguments
            print dir(msg[1])
            print msg[1].target
            print msg[1].source