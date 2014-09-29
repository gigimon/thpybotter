__author__ = 'Darwin'

import re
import logging

import config

import requests
from lxml import html

from base import BasePlugin


LOG = logging.getLogger("irc_lepra")


class IRCPlugin(BasePlugin):
    name = "lepra"
    enabled = True
    reg = re.compile(r'https://[\w.]*leprosorium.ru/comments/\d+/?(?:#\d+)*')

    def _validate(self, event):
        if self.is_pubmsg(event):
            if 'leprosorium.ru' in ' '.join(event.arguments):
                return True
        return False

    def _run(self, msg):
        urls = self.reg.findall(' '.join(msg[1].arguments))
        headers = {"User-Agent":
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        }

        LOG.debug("Found lepra urls: %s" % urls)
        for url in urls:

            LOG.info("Processing %s" % url)

            try:
                tree = html.fromstring(requests.get(url, headers=headers, cookies=config.LEPRA_COOKIES).content)
                comment_id = re.search("#(\d+)$", url)

                if comment_id:
                    post_root = tree.xpath("//div[@id=%s]" % comment_id.group(1))[0]
                    post_text = post_root.xpath(".//div[@class='c_body']")[0].text_content().strip()
                    user = post_root.xpath(".//a[@class='c_user']")[0].text
                else:
                    post_root = tree.xpath("//div[@class='dt']")[0]
                    post_text = post_root.xpath(".//div[@class='dti']")[0].text_content().strip()
                    user = tree.xpath("//div[@class='dd']")[0].xpath(".//a[@class='c_user']")[0].text

                pretty_text = self.colorize(user, post_text)
                for text in self.split(pretty_text, colorized=True):
                   msg[0].privmsg(msg[1].target, text)

            except Exception as e:
                LOG.warning("Problem in parsing page: %s" % e)
