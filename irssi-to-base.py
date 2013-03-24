#!/usr/bin/python

# Copyright (c) 2013, Ali Clark <ali@clark.gb.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
# Day, (N)?N Mon YYYY HH:MM:SS( +NNNN)?

timestamp_match = re.compile(r'^\d+$')
time_match = re.compile(r'^([0-2][0-9]):([0-5][0-9])(:([0-6][0-9]))?$')

def millistamp(t):
    r = timestamp_match.match(t)
    if r:
        return t + '000'

    r = time_match.match(t)
    if r:
        h = r.group(1)
        m = r.group(2)
        s = r.group(4)
        dt = datetime.datetime.now().replace(hour=int(h), minute=int(m), second=0, microsecond=0)
        if s != None:
            dt = dt.replace(second=int(s))
        return str(int(round(time.mktime(dt.timetuple()) * 1000)))

    return str(int(round(time.time() * 1000)))

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
    chatmatcher  = re.compile(r'([^\t]+\t)?([^'+'\x04'+']+) '+'\x04'+'8/<'+'\x04'+'g(.)'+'\x04'+'([gc]|(>/))([^'+'\x04'+']+)'+'\x04'+'g'+'\x04'+'8/>'+'\x04'+'g '+'\x04'+'e'+'(.*)')
    bopmatcher   = re.compile(r'([^\t]+\t)?([^'+'\x04'+']+) '+'\x04'+r'8/-'+'\x04'+r'=/([^'+'\x04'+']+)'+'\x04'+'8/:'+'\x04'+'5/([^'+'\x04'+']+)'+'\x04'+'8/-'+'\x04'+'g '+'(.*)')
    mematcher    = re.compile(r'([^\t]+\t)?([^'+'\x04'+']+) '+'\x04'+r'c \* ([^'+'\x04'+']+)'+'\x04'+'g (.*)')
    notifmatcher = re.compile(r'([^\t]+\t)?([^'+'\x04'+']+) '+'\x04'+'9/-'+'\x04'+'g!'+'\x04'+'9/-'+'\x04'+'g '+'\x04'+'3/'+'([^'+'\x04'+']+)'+'\x04'+'g (.*)')

    try:
        line = sys.stdin.readline()

        while line:
            r = chatmatcher.match(line)
            if r:
                line = chatconvert(r.group(1), r.group(2), r.group(3), r.group(6), r.group(7))

            else:
                r = bopmatcher.match(line)
                if r:
                    line = chatconvert(r.group(1), r.group(2), ' ', '-' + r.group(3) + ':' + r.group(4) + '-', r.group(5))

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
