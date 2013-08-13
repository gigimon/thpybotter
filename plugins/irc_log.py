__author__ = 'gigimon'

import re
import os
import logging
from datetime import datetime

import config
from base import BasePlugin


LOG = logging.getLogger("irc_log")


class IRCPlugin(BasePlugin):
    name = "txtlogging"
    enabled = True

    def __init__(self, *args, **kwargs):
        super(IRCPlugin, self).__init__(*args, **kwargs)
        self._log_files = {}

    def get_logfile(self, chan):
        if not chan in self._log_files:
            log_path = getattr(config, 'LOG_PATH', None)
            if log_path is None:
                log_path = os.path.realpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', 'logs'))
            log_path = os.path.join(log_path, chan)
            if not os.path.isdir(log_path):
                os.makedirs(log_path)
            log_file = open(os.path.join(log_path, datetime.now().strftime('%d%m%y.log')), 'a+')
            self._log_files[chan] = log_file
            return log_file
        elif chan in self._log_files:
            log_date = datetime.strptime(self._log_files[chan].name.split('/')[-1], '%d%m%y.log')
            if not log_date.day == datetime.now().day:
                self._log_files[chan].close()
                del(self._log_files[chan])
                return self.get_logfile(chan)
        return self._log_files[chan]

    def _validate(self, event):
        if self.is_pubmsg(event):
            return True
        return False

    def write_to_log(self, chan, author, message):
        log = self.get_logfile(chan)
        msg = u'%s|%s|%s\n' % (datetime.now().strftime('%H:%M:%S'), author, message)
        log.write(msg.encode('utf8'))
        log.flush()

    def _run(self, msg):
        self.write_to_log(msg[1].target, msg[1].source.nick, ' '.join(msg[1].arguments))