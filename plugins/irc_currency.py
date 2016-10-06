# -*- coding: utf-8 -*-

__author__ = 'Darwin'

import requests
import logging 

from lxml import html
from base import BasePlugin

LOG = logging.getLogger("irc_currency")


class IRCPlugin(BasePlugin):
    name = "Currency"
    enabled = True

    def _validate(self, event):
        if self.is_pubmsg(event):
            if u'!пиздец' in ' '.join(event.arguments):
                return True
        return False

    def _run(self, msg):
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
        }
        usd_url = "http://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=RUB"
        eur_url = "http://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=RUB"
        brent_url = "http://www.investing.com/commodities/brent-oil"

        try:
            usd_tree = html.fromstring(requests.Session().get(usd_url, headers=headers).content)
            eur_tree = html.fromstring(requests.Session().get(eur_url, headers=headers).content)
            brent_tree = html.fromstring(requests.Session().get(brent_url, headers=headers).content)

            usd = float(usd_tree.xpath("//span[@class='uccResultAmount']")[0].text.strip())
            eur = float(eur_tree.xpath("//span[@class='uccResultAmount']")[0].text.strip())
            brent = float(brent_tree.xpath("//span[@id='last_last']")[0].text)
            

            msg[0].privmsg(msg[1].target, u"\00310$ \00314%.2f \00310\u20AC \00314%.2f \00310OIL: \00314%.2f\00310$" % (usd, eur, brent))

        except Exception as e:
            LOG.warning("Problem in parsing page: %s" % e)
            msg[0].privmsg(msg[1].target, u"Что-то пошло не так... Наверно экономике совсем пиздец!")
