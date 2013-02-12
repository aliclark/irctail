#!/bin/sh

if [ ! -e /tmp/irssitail ]; then
    touch /tmp/irssitail
fi

tailf /tmp/irssitail | ./irc-chanformat.py | ./irc-chanshift.py | ./irssi-nameformat.py | ./irc-colorize.py >>/tmp/feed
