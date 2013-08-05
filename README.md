thpybotter - simple threaded python irc bot for #nnm channel
==========

Usage
======

```python
In [1]: from bot import IRCBot

In [2]: b = IRCBot(("filezz.ru", 5557),"#nnm", "testbot", "blablabot")

In [3]: b.start()
```

TODO:
=====

    Daemonize - start/stop daemon
    Logging - log working process
    Plugins - many many pluuugiiiins! (twitter via api, vk, admin, logs)