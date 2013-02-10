#!/usr/bin/python

from __future__ import print_function

import sys
import re

maxlen = 0
def checkmaxlen(s):
    global maxlen
    if len(s) > maxlen:
        maxlen = len(s)

hits = {}
def uplogs(color):
    if color not in hits:
        hits[color] = 0

    hits[color] += 1

counts = {'grey': 0, 'blue': 0, 'green': 0, 'cyan': 0, 'red': 0, 'magenta': 0}
pallette = {'grey': '\x38', 'blue': '\x39', 'green': '\x3a', 'cyan': '\x3b', 'red': '\x3c', 'magenta': '\x3d'}
users  = {}

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
            ((v == minn) and (minh != None) and ((ch(k) not in hits) or (hits[ch(k)] < minh)))):
            minc = k
            minn = v
            if ch(k) in hits:
                minh = hits[ch(k)]
            else:
                minh = None

    counts[minc] += 1
    return ch(minc)

def get_color(s):
    if s not in users:
        users[s] = pick_color()
    return users[s]

def gotname(before, name, after):
    # without leading operator tag
    namet = name[1:]
    checkmaxlen(name)
    color = get_color(namet)
    uplogs(color)
    colorized = color + name + '\x04\x67'

    for u,c in users.items():
        # this is not ideal because
        # a) one name may be a subset of another name
        # b) a name might be a subset of another word
        # unfortunately checking if the name is a substring of a word
        # is complicated by the fact that color codes contain normal
        # chars.
        #
        # TODO: check for names which are a subset of another
        after = after.replace(u, c + u + '\x04\x67')

    return before + ((maxlen - len(name)) * ' ') + colorized + after

def main():
    # try to match two columns and a 3rd name column
    namematcher = re.compile('^(\ *[^\ \t]+[\ \t]+[^\ \t]+\ )[^<]*<([^\w]+[^>]+)>(.*)')
    try:
        line = sys.stdin.readline()
        while line:
            result = namematcher.match(line)
            if result:
                # name is like '\x04g@\x04gNAME\x04g\x048/'
                # make it like '@NAME'
                line = gotname(result.group(1), result.group(2)[2] + result.group(2)[5:-5], result.group(3) + '\n')

            print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
