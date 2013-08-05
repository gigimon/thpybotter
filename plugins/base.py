import threading
from Queue import Queue


class BasePlugin(threading.Thread):
    name = "baseplugin"
    enabled = True

    def __init__(self, *args, **kwargs):
        super(BasePlugin, self).__init__(*args, **kwargs)
        self._queue = Queue()

    def __str__(self):
        return "Plugin: %s" % self.name

    def colorize(self, user, message):
        return "\00310%s: \00314%s\003" % (user, message)

    def is_pubmsg(self, event):
        if event.type == 'pubmsg':
            return True
        return False

    def is_privmsg(self, event):
        if event.type == 'privmsg':
            return True
        return False

    def _validate(self, event):
        return True

    def put(self, msg):
        if self._validate(msg[1]):
            self._queue.put(msg)

    def run(self):
        raise NotImplemented