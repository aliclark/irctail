#!/bin/sh

if [ ! -e /tmp/irctail ]; then
    touch /tmp/irctail
fi

tailf /tmp/irctail | ./irssi-chanformat.py | ./irssi-chanshift.py | ./base-nameformat.py | ./irc-timeformat.py | ./irssi-colorize.py >>/tmp/feed
