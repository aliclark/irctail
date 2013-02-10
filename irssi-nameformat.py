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

def gotname(before, name, after):
    global maxlen
    # without leading operator tag
    namet = name[1:]
    maxlen = il.getmaxlen(name, maxlen)
    color = il.getcolor(namet, allocated, counts, hits)
    il.uplogs(color, hits)

    for u,c in allocated.items():
        if u not in textmatcher:
            textmatcher[u] = re.compile('((\x04\x65)|([^\w])|(^))(' + re.escape(u) + ')(([^\w])|($))')

        after = re.sub(textmatcher[u], '\\1' + c + '\\5' + '\x04\x67' + '\\6', after)

    return before + il.getmaxpad(name, maxlen) + color + name + '\x04\x67' + after

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
