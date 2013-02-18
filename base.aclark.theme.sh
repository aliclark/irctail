#!/bin/sh

./irc-chanformat.py | ./irc-chanshift.py | ./base-nameformat.py | ./base-timeformat.py | ./irc-colorize.py
