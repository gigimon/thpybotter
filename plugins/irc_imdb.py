__author__ = 'Darwin'

import requests
from base import BasePlugin
import json
import logging 

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
            json_api=json.loads(requests.get(url).content)
            line1 = json_api['Title'] + " (" + json_api['Year'] + ") - " + imdb_url % json_api['imdbID'] + " | " + json_api['Genre'] 
            line2 = json_api['Plot']
            line3 = json_api['imdbRating'] + "/10 - (" + json_api['imdbVotes'] + " votes)" + " | " + json_api['Runtime'] 
            msg[0].privmsg(msg[1].target, line1)
            msg[0].privmsg(msg[1].target, line2)
            msg[0].privmsg(msg[1].target, line3)
        except Exception as e:
            LOG.warning("Problem in parsing page: %s" % e)
