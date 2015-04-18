Simple Websockets
=================

A simple pure python implementation of RFC6455 websockets.
Heavily based on https://gist.github.com/jkp/3136208.
As yet still quite incomplete but relative to that gist is 
at least (with-in the code at least) clearer about it's deficiencies
(i.e. it raises lots of NotImplementedErrors)

What's not done
---------------

* Receiving multi-frame messages
* Sending multi-frame messages
* All the control packet types.

Why?
----

This was intended as a development prop for doing some websocket 
development on windows when I couldn't be bothered to fight with 
compiling up gevent, uwsgi or any of the other tools websockets 
seem to be based. It was going to be for use with in flask which is
why there is a broken flask example. I was hopeful when starting that
I could produce an interface compatible with one of the more production
quality websocket servers, but that clearly isn't realistic. I'm tempted
to go the other way and standardise on this interface and produce
wrappers for the gevent uwsgi interfaces. That wouldn't be difficult
to do.

