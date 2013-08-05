import irc.bot

from plugins import load_plugins


class IRCBot(irc.bot.SingleServerIRCBot):

    def __init__(self, server, channels, nickname, realname,
                 reconnection_interval=60, **connect_params):
        super(IRCBot, self).__init__([server], nickname, realname, reconnection_interval, **connect_params)
        self._default_channels = channels if isinstance(channels, (list, tuple)) else [channels]
        self._plugins = load_plugins()

    def on_welcome(self, connect, event):
        for ch in self._default_channels:
            connect.join(ch)

    def _message_process(self, connect, event):
        for plugin in self._plugins:
            plugin.put((connect, event))

    def on_privmsg(self, connect, event):
        self._message_process(connect, event)

    def on_pubmsg(self, connect, event):
        self._message_process(connect, event)

    def start(self):
        for p in self._plugins:
            p.start()
        super(IRCBot, self).start()