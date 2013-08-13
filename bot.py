import logging

import irc.bot

from plugins import load_plugins


LOG = logging.getLogger()


class IRCBot(irc.bot.SingleServerIRCBot):

    def __init__(self, server, channels, nickname, realname,
                 reconnection_interval=60, **connect_params):
        super(IRCBot, self).__init__([server], nickname, realname, reconnection_interval, **connect_params)
        LOG.info("Initialize Bot instance")
        self._default_channels = channels if isinstance(channels, (list, tuple)) else [channels]
        self._plugins = []

    def on_welcome(self, connect, event):
        for ch in self._default_channels:
            LOG.info("Connect to channel %s" % ch)
            connect.join(ch)

    def _message_process(self, connect, event):
        LOG.debug("Process message: %s" % event.arguments)
        if event.source.nick == self.connection.get_nickname():
            LOG.debug("It's my message!")
            return
        for plugin in self._plugins:
            plugin.put((connect, event))

    def on_privmsg(self, connect, event):
        self._message_process(connect, event)

    def on_pubmsg(self, connect, event):
        self._message_process(connect, event)

    def start(self):
        LOG.info("Start bot")
        LOG.info("Load plugins")
        plugins = load_plugins()
        LOG.info("Loaded plugins: %s" % self._plugins)
        for p in plugins:
            LOG.info('Initialize plugin: %s' % p.name)
            p = p(self.connection, self.channels)
            LOG.info("Start plugin %s" % p)
            p.start()
            self._plugins.append(p)
        LOG.info("Start loop")
        super(IRCBot, self).start()

    def die(self):
        LOG.info("Destroy bot")
        for p in self._plugins:
            p.stop()
            p.join()
        super(IRCBot, self).die("Bye!")