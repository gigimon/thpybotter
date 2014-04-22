__author__ = 'gigimon'

import re
import logging

import tweepy
from tweepy.streaming import Stream, StreamListener, API

import config
from base import BasePlugin


LOG = logging.getLogger("irc_twi_stream")


class StreamerToIrc(StreamListener):
    def __init__(self, parent, *args, **kwargs):
        self._parent = parent
        super(StreamerToIrc, self).__init__(*args, **kwargs)

    def on_status(self, status):
        for chan in self._parent._channels:
            LOG.debug("Send message to %s %s" % (chan, status.text))
            tweet_text = self._parent.colorize("%s @%s" % (status.user.name, status.user.screen_name),
                                               status.text.replace('\n', ' '))
            self._parent._connection.privmsg(chan, tweet_text)
        return


class IRCPlugin(BasePlugin):
    name = "twitter_stream"
    enabled = True

    def _validate(self, event):
        return False

    def stop(self):
        if self._stream:
            self._stream.disconnect()

    def run(self):
        try:
            auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(config.TWITTER_ACCESS_KEY, config.TWITTER_ACCESS_SECRET)
            self._stream = Stream(auth, StreamerToIrc(self))
            LOG.info("Twitter stream successfully initializing")
        except Exception as e:
            LOG.error("Twitter stream authorization failed: %s" % e)
            return
        followers = []
        api = API(auth)
        for f in config.TWITTER_FOLLOW_IDS:
            if isinstance(f, (str, unicode)):
                try:
                    user_id = api.get_user(f).id
                    followers.append(str(user_id))
                except Exception:
                    LOG.debug("Can't get ID for %s" % user_id)
                    continue
            else:
                followers.append(str(f))
        self._stream.filter(followers)
