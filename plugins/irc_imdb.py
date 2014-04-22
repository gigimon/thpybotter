# -*- coding: utf-8 -*-
__author__ = 'Darwin'

import requests
import logging 

from base import BasePlugin

LOG = logging.getLogger("irc_imdb")


class IRCPlugin(BasePlugin):
    name = "imdb"
    enabled = True

    def _validate(self, event):
        if self.is_pubmsg(event):
            if 'imdb' in ' '.join(event.arguments):
                return True
        return False

    def _run(self, msg):
        try:
            name = " ".join(msg[1].arguments[0].split(" ")[1:])
            url = "http://www.omdbapi.com/?t=%s" % name
            imdb_url = "http://www.imdb.com/title/%s/"
            json_api=requests.get(url).json()
            line1 = u"\x02%s\x02 (%s) - %s | %s" % (json_api['Title'], json_api['Year'], imdb_url % json_api['imdbID'], json_api['Genre'])
            line2 = json_api['Plot'][:460]
            line3 = u"\x033 %s/10 - (%s votes) | %s" % (json_api['imdbRating'], json_api['imdbVotes'], json_api['Runtime'])
            msg[0].privmsg(msg[1].target, line1)
            msg[0].privmsg(msg[1].target, line2)
            msg[0].privmsg(msg[1].target, line3)
        except Exception as e:
            LOG.warning("Problem in parsing page: %s" % e)
            msg[0].privmsg(msg[1].target, u"Нет такого фильма, извини :(")
