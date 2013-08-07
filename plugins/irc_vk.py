__author__ = 'Darwin'

import re
import logging

import requests
from bs4 import BeautifulSoup

from base import BasePlugin


LOG = logging.getLogger("irc_vkontakte")


class IRCPlugin(BasePlugin):
    name = "vkontakte"
    enabled = True
    reg = re.compile(r'((?:http|https)://vk.com/wall[-\d_\d]+)')

    def _validate(self, event):
        if self.is_pubmsg(event):
            if 'vk.com' in ' '.join(event.arguments):
                return True
        return False

    def _split(self, message):
        for i in range(0, len(message), 300):
            yield message[i:i+300]
      
    def _run(self, msg):
        urls = self.reg.findall(' '.join(msg[1].arguments))
        LOG.debug("Find vkontakte urls: %s" % urls)
        for url in urls:
            LOG.info("Processing %s" % url)
            try:
                soup = BeautifulSoup(requests.get(url).content)
                post_text = soup.find("div", class_="wall_post_text").text
                author = soup.find("a", class_="fw_post_author").text
                likes = soup.find("span", class_="fw_like_count fl_l").text

                pretty_text = self.colorize(author, post_text, likes)
                for text in self._split(pretty_text):
                    msg[0].privmsg(msg[1].target, text)
            except Exception as e:
                LOG.warning("Problem in parsing page: %s" % e)
