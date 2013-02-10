#!/bin/sh

if [ ! -e /tmp/irssitail ]; then
    touch /tmp/irssitail
fi

tailf /tmp/irssitail | ./irssi-chanformat.py | ./irssi-chanshift.py | ./irssi-nameformat.py | ./irssi-colorize.py >>/tmp/feed
