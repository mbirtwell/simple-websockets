""" Main file for running example app with werkzeug server

Works OK. Werkzeug will put an extra Connection: close header
in to the handshake responses. Tested with IE and Chrome this
gets ignored.
"""
import os

from werkzeug.serving import run_simple

os.environ['WSGI_SERVER'] = 'werkzeug'
from example_app import application

run_simple('127.0.0.1', 8002, application, threaded=True)

