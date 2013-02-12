#!/bin/sh

if [ ! -e /tmp/irssitail ]; then
    touch /tmp/irssitail
fi

tailf /tmp/irssitail | ./irssi-chanformat.py | ./irssi-chanshift.py | ./irssi-nameformat.py | ./irc-colorize.py >>/tmp/feed
