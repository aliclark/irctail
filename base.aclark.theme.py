#!/bin/sh

if [ ! -e /tmp/irctail ]; then
    touch /tmp/irctail
fi

tailf /tmp/irctail | ./irc-chanformat.py | ./irc-chanshift.py | ./base-nameformat.py | ./base-timeformat.py | ./irc-colorize.py >>/tmp/feed
