#!/bin/sh

./irc-chanformat.py | ./irc-chanshift.py | ./irssi-nameformat.py | ./irc-colorize.py
