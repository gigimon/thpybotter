import os
from datetime import datetime

import tornado.ioloop
import tornado.web

from sockjs.tornado import SockJSConnection, SockJSRouter, proto

from config import LOG_DIR


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('static/index.html')


class LogViewerHandler(SockJSConnection):
    def on_message(self, message):
        message = proto.json_decode(message)
        if 'channel' in message:
            self._channel = message['channel']
            self._start_view_log()
            self.loop = tornado.ioloop.PeriodicCallback(self._check_new_message, 1000)
            self.loop.start()

    def _start_view_log(self):
        log_path = LOG_DIR
        if log_path is None:
            log_path = os.path.realpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'logs'))
        log_path = os.path.join(log_path, self._channel, datetime.now().strftime('%Y'), datetime.now().strftime('%m'))
        self._log = os.path.join(log_path, datetime.now().strftime('%d%m%y.log'))
        if not os.path.isfile(self._log):
            self.send(proto.json_encode({'error': 'Not found logs'}))
        self._last_check = os.stat(self._log)[8]
        self._last_seek = 0
        self._send_new_messages()

    def _send_new_messages(self):
        with open(self._log) as f:
            f.seek(self._last_seek)
            messages = f.readlines()
            res = []
            for m in messages:
                msg = m.split('|')
                res.append({
                    'date': msg[0],
                    'user': msg[1],
                    'message': '|'.join(msg[2:])
                })
            self._last_seek = f.tell()
            self.send(proto.json_encode(res))

    def _check_new_message(self):
        if not os.stat(self._log)[8] == self._last_check:
            self._last_check = os.stat(self._log)[8]
            self._send_new_messages()

LogRouter = SockJSRouter(LogViewerHandler, '/logs')

if __name__ == '__main__':
    app = tornado.web.Application(
        [(r"/", IndexHandler)] +
        LogRouter.urls
    )
    app.listen(8080)

    print 'Listening on 0.0.0.0:8080'

    tornado.ioloop.IOLoop.instance().start()