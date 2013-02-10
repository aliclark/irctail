#!/usr/bin/python

from __future__ import print_function

import sys
import re
import irssilib as il

maxlen = 0
hits = {}

counts = {'grey': 0, 'blue': 0, 'green': 0, 'cyan': 0, 'red': 0, 'magenta': 0}
allocated  = {}

textmatcher = {}

def format_chan(after, channel=None):
    global maxlen
    chanstr = ''

    if channel != None:
        maxlen = il.getmaxlen(channel, maxlen)
        chancolor = il.getcolor(channel, allocated, counts, hits)
        il.uplogs(chancolor, hits)
        chanstr = il.getmaxpad(channel, maxlen) + chancolor + channel + il.clearseq + ' '

        for u,c in allocated.items():
            if u not in textmatcher:
                textmatcher[u] = re.compile('((' + il.crankseq + ')|([^\w])|(^))(' + re.escape(u) + ')(([^\w])|($))')

            after = re.sub(textmatcher[u], '\\1' + c + '\\5' + il.clearseq + '\\6', after)

    return chanstr + after

def main():
    chanmatcher = re.compile('^((#[^\t]+)\t)?(.*)')
    try:
        line = sys.stdin.readline()
        while line:
            result = chanmatcher.match(line)
            if result:
                line = format_chan(result.group(3) + '\n', result.group(2))
            print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
