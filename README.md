Simple Websockets
=================

A simple websocket implementation and abstraction. 

This provides a (still somewhat incomplete) pure python implementation 
of websockets, with minimal dependencies. And a couple of shims with the 
same interface to implementations based on existing servers.

It's compatible withe the following servers:
* uWSGI (python 2 and python 3)
* Gunicorn (with gevent-websocket python 2 only due to dependency on gevent)
* Werkzeug's development server (python 2 and python 3)
* wsgiref (python 2 and python 3)
* http.server from the python 3 standard library

See example/example_app with uWSGI, Gunicorn and werkzeug. Other examples are
available in example. See below for caveats about working with the various servers.

My websocket implementation
---------------------------

My websocker implementation is a simple pure python implementation of RFC6455 websockets.
Heavily based on https://gist.github.com/jkp/3136208.
As yet still quite incomplete but relative to that gist is 
at least (with-in the code at least) clearer about it's deficiencies
(i.e. it raises lots of NotImplementedErrors)

What's not done
---------------

* Receiving multi-frame messages
* Sending multi-frame messages
* Ping/pong control packets

Why?
----

This was intended as a development prop for doing some websocket 
development on windows when I couldn't be bothered to fight with 
compiling up gevent, uwsgi or any of the other tools websockets 
seem to be based. I was hopeful when starting that
I could produce an interface compatible with one of the more production
quality websocket servers, but that clearly isn't realistic. So, I've 
built the wrappers for uwsgi and gevent. This allows me to have a single
source app which runs on werkzeug's development server on my windows laptop
and on uwsgi for "production".

Caveats
-------

uWSGI: The main potential problem with this is the error reporting. Looking at
the code it appears that if you can't receive a message for what ever reason 
including a graceful close from the other end you get the same exception. I've
been a bit optimistic and interpreted that exception as close.

Werkzeug: The werkzeug server not unreasonably follows the wsgi standard and ignores
the "Connection: upgrade" header sent by my websocket implementation and sends its 
own "Connection: close" header. This gets ignored by all the browsers I've tried so
far so everything works, but it's not ideal.

wsgiref: Also follows the wsgi standard. But more strictly than werkzeug and so needs
a minor monkeypatch to work. This is applied automatically if you use
websockets.get_impl_for_wsgi_server('wsgiref').

