# -*- coding: utf-8 -*-
# Yandex calculator parser


__author__ = 'Darwin'

import requests
import logging 
import re

from lxml import html
from base import BasePlugin

LOG = logging.getLogger("irc_yandexcalc")


class IRCPlugin(BasePlugin):
    name = "YandexCalc"
    enabled = True

    def _validate(self, event):
        if self.is_pubmsg(event):
            if '%' in ' '.join(event.arguments):
                return True
        return False

    def _run(self, msg):
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
        }
        req_str = " ".join(msg[1].arguments[0].split(" ")[1:])
        url = "http://yandex.ru/yandsearch?lr=14&text=%s" % req_str
        
        try:
            tree = html.fromstring(requests.Session().get(url, headers=headers).content)
            data = tree.xpath("//div[contains(@class, 'z-converter__data z-converter_nodata')]")[0].text_content()
            # Making UTF-8 numbers float and rounding them.
            data = re.sub("([,\d]+)", lambda m: "%s" % float(m.group(0).replace(",", ".")), data)
            msg[0].privmsg(msg[1].target, data.encode("utf-8"))

        except Exception as e:
            LOG.warning("Problem in parsing page: %s" % e)
            #msg[0].privmsg(msg[1].target, u"Что-то пошло не так...")
