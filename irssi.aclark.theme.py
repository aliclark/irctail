#!/bin/sh

tailf /tmp/irssitail | ./irssi-chanformat.py | ./irssi-colorize.py >>/tmp/feed
