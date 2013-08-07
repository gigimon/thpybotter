import os
import signal
import logging
from optparse import OptionParser

import lockfile
import daemon

import log
import config
from bot import IRCBot

LOG = logging.getLogger('main')

ircbot = IRCBot(config.SERVER, config.CHANNELS, config.NICKNAME, config.REALNAME)


def destroy(*args):
    LOG.info("Destroy IRC Bot by signal")
    ircbot.die()


def run_daemonize():
    context = daemon.DaemonContext(
        working_directory=os.path.realpath(os.path.curdir),
        pidfile=lockfile.FileLock('daemon')
    )
    context.signal_map = {
        signal.SIGTERM: destroy
    }
    context.stdout = open('stdout.log', 'wr')
    context.stderr = open('stderr.log', 'wr')

    with context:
        ircbot.start()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--daemonize", dest="daemonize", help="Daemonize bot or not", action="store_true")
    (options, args) = parser.parse_args()

    if options.daemonize:
        LOG.info("Run bot in daemonize mode")
        run_daemonize()
    else:
        LOG.info("Run bot in standalone mode")
        signal.signal(signal.SIGINT, destroy)
        ircbot.start()