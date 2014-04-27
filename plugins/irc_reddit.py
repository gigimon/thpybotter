__author__ = 'Darwin'

import re
import logging

import reddit

from base import BasePlugin


LOG = logging.getLogger("irc_reddit")


class IRCPlugin(BasePlugin):
    name = "reddit"
    enabled = True
    # I'm not sure this is right, gigimon, please take a look at it and fix it
    reg = re.compile(r'(http://(?:www.)?reddit.com/r/(.+))')
    def _validate(self, event):
        if self.is_pubmsg(event):
            if 'reddit.com' in ' '.join(event.arguments):
                return True
        return False

    def _run(self, msg):
        urls = self.reg.findall(' '.join(msg[1].arguments))
        LOG.debug("Found reddit urls: %s" % urls)

        for url in urls:
            # gigimon, fix this ASAP
            url = url[0] 
            LOG.info("Processing %s" % url)

            try:
                reddit_json = reddit.parse(url)

                try:
                    post_text = reddit_json['selftext'].replace("\n", " ")
                except KeyError:
                    post_text = reddit_json['body'].replace("\n", " ")

                pretty_text = self.colorize(reddit_json['author'], post_text,
                        ups=reddit_json['ups'], downs=reddit_json['downs'])
                for text in self.split(pretty_text, colorized=True):
                    msg[0].privmsg(msg[1].target, text)
            except Exception as e:
                LOG.warning("Problem in parsing page: %s" % e)
