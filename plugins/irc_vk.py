__author__ = 'Darwin'

import re
import logging

import requests
from lxml import html

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
        headers={"User-Agent":
                     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        }
        LOG.debug("Find vkontakte urls: %s" % urls)
        for url in urls:
            LOG.info("Processing %s" % url)
            try:
                tree = html.fromstring(requests.get(url, headers=headers).content)
                post_text = tree.xpath("//div[contains(@class, 'wall_post_text')]")
                if post_text:
                    post_text = post_text[0].text_content()
                else:
                    LOG.warning("Can't get post content in url %s" % url)
                    continue
                author = tree.xpath("//a[contains(@class, 'fw_post_author')]")[0].text
                likes = tree.xpath("//span[contains(@class, 'fw_like_count')]")[0].text

                pretty_text = self.colorize(author, post_text, likes)
                for text in self._split(pretty_text):
                    msg[0].privmsg(msg[1].target, text)
            except Exception as e:
                LOG.warning("Problem in parsing page: %s" % e)
