import os
import signal
from optparse import OptionParser

import lockfile
import daemon

import config
from bot import IRCBot


ircbot = IRCBot(config.SERVER, config.CHANNELS, config.NICKNAME, config.REALNAME)


def destroy(*args):
    ircbot.die()


def run_daemonize():
    context = daemon.DaemonContext(
        working_directory=os.path.realpath(os.path.curdir),
        pidfile=lockfile.FileLock('daemon')
    )
    context.signal_map = {
        signal.SIGTERM: destroy
    }
    with context:
        ircbot.start()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--daemonize", dest="daemonize", help="Daemonize bot or not", action="store_true")
    (options, args) = parser.parse_args()

    if options.daemonize:
        run_daemonize()
    else:
        ircbot.start()