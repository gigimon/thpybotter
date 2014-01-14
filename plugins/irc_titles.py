__author__ = 'Darwin'

import re
import logging

import requests
from lxml import html

from base import BasePlugin


LOG = logging.getLogger("irc_titles")


class IRCPlugin(BasePlugin):
    name = "titles"
    enabled = True
    url_reg = r'((https?:\/\/)([\da-zA-Z\.-]+)\.([a-z\.]{2,6})([\/\w\d\.-\?%&;]*))'
    url_reg = re.compile(url_reg)

    def _validate(self, event):
        if self.is_pubmsg(event):
            for url in self.url_reg.findall(' '.join(event.arguments)):
                if 'vk.com/' not in url[0]:
                    return True
        return False

    def _split(self, message):
        for i in range(0, len(message), 250):
            yield message[i:i+250]
      
    def _run(self, msg):
        urls = self.url_reg.findall(' '.join(msg[1].arguments))
        headers = {"User-Agent":
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        }
        for url_tuple in urls:
            url = url_tuple[0]
            LOG.info("Processing %s" % url)
            try:
                tree = html.fromstring(requests.get(url, headers=headers).content)
                title = tree.xpath('//title/text()')[0]
                msg[0].privmsg(msg[1].target, u'\u0002Title:\u0002 ' + title)
            except Exception as e:
                LOG.warning("Problem in parsing page: %s" % e)
