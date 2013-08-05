import os
import glob


def load_plugins():
    plugins = []
    loc = os.path.abspath(os.path.dirname(__file__))
    for m in glob.glob(os.path.join(loc, 'irc_*.py')):
        name = m.split('.')[0].split('/')[-1]
        plugin = __import__(name, globals(), locals(), ['IRCPlugin'])
        plugin = getattr(plugin, 'IRCPlugin', None)
        if plugin and plugin.enabled:
            plugin = plugin()
            plugins.append(plugin)
    return plugins