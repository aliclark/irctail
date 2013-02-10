#!/bin/sh

tailf /tmp/irssitail | ./irssi-chanformat.py | ./irssi-chanshift.py | ./irssi-colorize.py >>/tmp/feed
