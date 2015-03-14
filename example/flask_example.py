"""Attempt to make my web socket implementation work with flask

It Doesn't

The problem is that flask tries to force our wsgi application
to be a response object. Which requires buffering the response.
"""
from flask import Flask, send_file

from websockets.flask_router import ws_route


app = Flask(__name__)


@app.route('/')
def index():
    return send_file('index.html')


@ws_route(app, '/test_path')
def pong_handler(websocket):
    while True:
        msg = websocket.read_message()
        websocket.send_message("Pong from flask: " + msg)


if __name__ == '__main__':
    app.run(threaded=True)
