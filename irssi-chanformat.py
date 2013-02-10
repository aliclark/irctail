#!/usr/bin/python

from __future__ import print_function

import sys
import re

maxlen = 0
def checkmaxlen(s):
    global maxlen
    if len(s) > maxlen:
        maxlen = len(s)

chanhits = {}
def uplogs(chancolor):
    if chancolor not in chanhits:
        chanhits[chancolor] = 0

    chanhits[chancolor] += 1

counts = {'grey': 0, 'blue': 0, 'green': 0, 'cyan': 0, 'red': 0, 'magenta': 0}
pallette = {'grey': '\x38', 'blue': '\x39', 'green': '\x3a', 'cyan': '\x3b', 'red': '\x3c', 'magenta': '\x3d'}
chans  = {}

def ch(c):
    return '\x04' + pallette[c] + '\x2f'

def pick_color():
    minc = None
    minn = None
    minh = None

    for (k,v) in counts.items():
        # Modified the color picking algorithm from basic round-robin:
        # In case of ties, give the color which appears to be least commonly used.
        # This is roughly as good as it gets, since we have no
        # information about the channel we are assigning a new colour
        # for.
        # Could be slightly cleverer about resilience against a
        # one-off burst on a different colour, but meh.
        # This will also happily assign a colour which has been seen
        # in the last line on a different channel, but that's probably coincidence.
        # Perhaps this should consider consecutive lines from the same
        # channel to be a single hit.

        if ((minn == None) or (v < minn) or
            ((v == minn) and (minh != None) and ((ch(k) not in chanhits) or (chanhits[ch(k)] < minh)))):
            minc = k
            minn = v
            if ch(k) in chanhits:
                minh = chanhits[ch(k)]
            else:
                minh = None

    counts[minc] += 1
    return ch(minc)

def chan_color(s):
    if s not in chans:
        chans[s] = pick_color()
    return chans[s]

def format_chan(text, channel=None):
    chanstr = ''

    if channel != None:
        checkmaxlen(channel)
        chancolor = chan_color(channel)
        uplogs(chancolor)
        chanstr = ((maxlen - len(channel)) * ' ') + chancolor + channel + '\x04\x67' + ' '

    return chanstr + text

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
