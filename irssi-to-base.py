#!/usr/bin/python

from __future__ import print_function

import sys
import re
import datetime
import time

# You'll need the following in ~/.irssi/config:
# log_timestamp = "%s ";
#
# Allowing more types of log format could take some work
# Other good formats to support would be:
# YYYY-mm-DD HH:MM:SS( +NNNN)?
# HH:MM(:SS)?
def millistamp(timestamp):
    return timestamp + '000'

def chatconvert(chan, ts, perm, name, text):
    if not chan:
        chan = ''
    if perm == ' ':
        perm = ''
    return chan + millistamp(ts) + '\t' + perm + name + '\t' + text + '\n'

def notifconvert(chan, ts, name, text):
    if not chan:
        chan = ''
    return chan + millistamp(ts) + '\t--- ' + name + '\t' + text + '\n'

def meconvert(chan, ts, name, text):
    if not chan:
        chan = ''
    return chan + millistamp(ts) + '\t* ' + name + '\t' + text + '\n'

def main():
    chatmatcher  = re.compile(r'([^\t]+\t)?(\d+) '+'\x04'+'8/<'+'\x04'+'g(.)'+'\x04'+'g([^'+'\x04'+']+)'+'\x04'+'g'+'\x04'+'8/>'+'\x04'+'g '+'\x04'+'e'+'(.*)')
    mematcher    = re.compile(r'([^\t]+\t)?(\d+) '+'\x04'+r'c \* ([^'+'\x04'+']+)'+'\x04'+'g (.*)')
    notifmatcher = re.compile(r'([^\t]+\t)?(\d+) '+'\x04'+'9/-'+'\x04'+'g!'+'\x04'+'9/-'+'\x04'+'g '+'\x04'+'3/'+'([^'+'\x04'+']+)'+'\x04'+'g (.*)')

    try:
        line = sys.stdin.readline()
        while line:
            r = chatmatcher.match(line)
            if r:
                line = chatconvert(r.group(1), r.group(2), r.group(3), r.group(4), r.group(5))
            else:
                r = notifmatcher.match(line)
                if r:
                    line = notifconvert(r.group(1), r.group(2), r.group(3), r.group(4))
                else:
                    r = mematcher.match(line)
                    if r:
                        line = meconvert(r.group(1), r.group(2), r.group(3), r.group(4))

            print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
