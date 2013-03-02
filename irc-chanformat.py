#!/usr/bin/python

from __future__ import print_function

import sys
import re
import irssilib as il

maxlen = 0
hits = {}

counts = {}
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
        after = il.text_colorize(after, textmatcher, allocated)

    return chanstr + after

# TODO: even if no match, perform colorization of text

def main():
    chanmatcher = re.compile('^((#?[^\t]+)\t)?(.*)')
    try:
        line = sys.stdin.readline()
        while line:
            result = chanmatcher.match(line)
            if result:
                line = format_chan(result.group(3) + '\n', result.group(2))
            else:
                line = il.text_colorize(line, textmatcher, allocated)
            print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
