__author__ = 'gigimon'

import re
import logging

import tweepy
import config
from base import BasePlugin


LOG = logging.getLogger("irc_twitter")


class IRCPlugin(BasePlugin):
    name = "twitter"
    enabled = True
    reg = re.compile(r'((?:http|https)://twitter.com/.+/status/\d+)')

    def __init__(self, *args, **kwargs):
        super(IRCPlugin, self).__init__(*args, **kwargs)
        try:
            auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(config.TWITTER_ACCESS_KEY, config.TWITTER_ACCESS_SECRET)
            self._api = tweepy.API(auth)
            LOG.info("Twitter successfully initializing")
        except Exception as e:
            LOG.error("Twitter authorization failed: %s" % e)
            self._api = None

    def _validate(self, event):
        if self.is_pubmsg(event):
            if 'twitter.com' in ' '.join(event.arguments):
                return True
        return False

    def _run(self, msg):
        if not self._api:
            return
        urls = self.reg.findall(' '.join(msg[1].arguments))
        for url in urls:
            id = re.findall(r"(\d+)$", url.strip())
            if not id:
                continue
            message = self._api.get_status(id[0].strip())
            tweet_text = self.colorize("%s @%s" % (message.user.name, message.user.screen_name),
                                       message.text.replace('\n', ' '))
            msg[0].privmsg(msg[1].target, tweet_text)
