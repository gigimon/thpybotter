# -*- coding: utf-8 -*-
__author__ = 'Darwin'

import logging 
import kinopoisk

from base import BasePlugin

LOG = logging.getLogger("irc_kinopoisk")


class IRCPlugin(BasePlugin):
    name = "kinopoisk"
    enabled = True

    def _validate(self, event):
        if self.is_pubmsg(event):
            if u'!кино' in ' '.join(event.arguments):
                return True
        return False

    def _split(self, message):
        for i in range(0, len(message), 250):
            yield message[i:i+250]

    def _run(self, msg):
        try:
            name = " ".join(msg[1].arguments[0].split(" ")[1:])
            kino = kinopoisk.Kinopoisk()
            movie = kino.search_movie(name)
            line1 = u"\x02%s\x02 (%s) - %s | %s" % (movie['name'], movie['altname'], movie['year'], movie['genre'])
            line2 = movie['description']
            if movie['top250']:
                line3_skelet = u"\x02Top250: "+movie['top250']+"\x02 | \x033 %s/10 - (%s votes) | %s - %s"
            else:
                line3_skelet = u"\x033 %s/10 - (%s votes) | %s - %s"
            line3 = line3_skelet % (movie['rating'], movie['ratingCount'], movie['duration'], movie['url'])
            msg[0].privmsg(msg[1].target, line1)
            for text in self._split(line2):
                msg[0].privmsg(msg[1].target, text)
            msg[0].privmsg(msg[1].target, line3)
        except Exception as e:
            LOG.warning("Problem in parsing page: %s" % e)
            msg[0].privmsg(msg[1].target, u"Нет такого фильма, извини :(")
