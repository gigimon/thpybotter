import os
import sys
import signal
import logging
from optparse import OptionParser

import lockfile
import daemon

import log
import config
from bot import IRCBot

LOG = logging.getLogger('main')

LOCK = lockfile.FileLock('thbotter')

ircbot = IRCBot(config.SERVER, config.CHANNELS, config.NICKNAME, config.REALNAME)


def destroy(*args):
    LOG.info("Destroy IRC Bot by signal")
    ircbot.die()


def run_daemonize():
    LOG.debug("Start initialize daemon")
    bot_path = os.path.realpath(os.path.dirname(__file__))
    context = daemon.DaemonContext(
        working_directory=bot_path,
        pidfile=LOCK
    )
    LOG.debug("Add signals map")
    context.signal_map = {
        signal.SIGTERM: destroy
    }
    LOG.debug("Change stdout/stderr")
    context.stdout = open(os.path.join(bot_path, 'stdout.log'), 'wr')
    context.stderr = open(os.path.join(bot_path, 'stderr.log'), 'wr')
    context.files_preserve = [LOG.parent.handlers[0].stream.fileno()]

    LOG.debug("Start bot")
    with context:
        LOG.info("Run bot loop")
        try:
            ircbot.start()
        except:
            for p in ircbot._plugins:
                if p.is_alive():
                    p.stop()
                    p.join()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--daemonize", dest="daemonize", help="Daemonize bot or not", action="store_true")
    (options, args) = parser.parse_args()

    if options.daemonize:
        if os.path.isfile(LOCK.lock_file):
            print "Please delete lock file: %s" % LOCK.lock_file
            sys.exit(1)
        LOG.info("Run bot in daemonize mode")
        run_daemonize()
    else:
        LOG.info("Run bot in standalone mode")
        signal.signal(signal.SIGINT, destroy)
        ircbot.start()