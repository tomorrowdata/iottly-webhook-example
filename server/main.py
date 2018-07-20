# Copyright 2018 TomorrowData Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
from collections import Counter
from datetime import datetime

import tornado.ioloop
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.websocket import WebSocketHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s'
                    )

message_counter = Counter(received = 0)
first_request = {'timestamp': None}

class UserWebHookHandler(RequestHandler):
    def post(self):
        if not first_request['timestamp']:
            first_request['timestamp'] = datetime.utcnow()

        message_counter.update(received = 1)

        payload = json.loads(self.request.body)
        logging.info('{} - {} - {}'.format(first_request['timestamp'], payload['msg']['timestamp'], message_counter['received']))

        msg = {
            'device': payload['msg']['from'],
            'deviceTimestamp': payload['msg']['devicetimestamp'],
            'payload': payload['msg']['payload']
        }

        WebHookForwarder.forward_to_clients(msg)


class WebHookForwarder(WebSocketHandler):
    ws_clients = set()

    def open(self):
        logging.info("New ws connection from: %s" % self.request.remote_ip)
        WebHookForwarder.ws_clients.add(self)

    def on_close(self):
        logging.info("Closing ws connection to %s" % self.request.remote_ip)
        try:
            WebHookForwarder.ws_clients.remove(self)
        except KeyError:
            pass

    @classmethod
    def forward_to_clients(cls, msg):
        logging.info("Sending message to %d clients", len(cls.ws_clients))
        for client in cls.ws_clients:
            try:
                client.write_message(msg)
            except:
                logging.error("Error sending message", exc_info=True)


def make_app():
    return Application([
        # Webhook handlers (called by iottly)
        (r"/webhook/user", UserWebHookHandler),
        # Web-socket
        (r"/ws/?", WebHookForwarder),
        # Serve client (HTML + Js)
        (r"/(.*)", StaticFileHandler, {
            "path": "app/client/",
            "default_filename": "index.html"
        }),
    ],
    debug=True,
    serve_traceback=True,
    autoreload=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()
