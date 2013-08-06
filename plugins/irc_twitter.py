__author__ = 'gigimon'

import re
from itertools import chain
from Queue import Empty

from lxml import html, etree
import requests

from base import BasePlugin


class IRCPlugin(BasePlugin):
    name = "twitter"
    enabled = True
    reg = re.compile(r'((?:http|https)://twitter.com/.+/status/\d+)')

    def _validate(self, event):
        if self.is_pubmsg(event):
            if 'twitter.com' in ' '.join(event.arguments):
                return True
        return False

    def stringify_children(self, node):
        parts = ([node.text] +
                 list(chain(*([c.text, etree.tostring(c, encoding='unicode'), c.tail] for c in node.getchildren()))) +
                 [node.tail])
        return ''.join(filter(None, parts))

    def _run(self, msg):
        urls = self.reg.findall(' '.join(msg[1].arguments))
        for url in urls:
            tree = html.fromstring(requests.get(url).content.decode('utf-8'))
            tweet = tree.xpath("//p[contains(@class, 'tweet-text')]")[0]
            tweet_name = '@'+tree.xpath("//span[contains(@class, 'username js-action-profile-name')]/b")[0].text
            realname = tree.xpath("//strong[contains(@class, 'fullname js-action-profile-name')]")[0].text
            etree.strip_tags(tweet, 's', 'a', 'span', 'b')
            tweet_parts = self.stringify_children(tweet)
            tweet_text = self.colorize("%s (%s)" % (tweet_name, realname), tweet_parts.strip())
            msg[0].privmsg(msg[1].target, tweet_text)
