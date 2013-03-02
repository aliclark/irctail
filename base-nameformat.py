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

def gotname(before, name, after, leadstr=None):
    global maxlen
    namet = name
    if not leadstr:
        leadstr = ''
    maxlen = il.getmaxlen(leadstr + name, maxlen)
    color = il.getcolor(namet, allocated, counts, hits)
    il.uplogs(color, hits)
    after = il.text_colorize(after, textmatcher, allocated)
    return before + il.getmaxpad(leadstr + name, maxlen) + leadstr + color + name + il.clearseq + after

def main():
    # try to match two columns and a 3rd name column
    namematcher = re.compile('^(\ *[^\ \t]+[\ \t]+[^\ \t]+)[\ \t]((---|\*)\ )?([^\w]*[^\ \t]+)[\ \t](.*)')
    try:
        line = sys.stdin.readline()
        while line:
            result = namematcher.match(line)
            if result:
                line = gotname(result.group(1) + ' ', result.group(4), ' ' + result.group(5) + '\n', result.group(2))
            else:
                line = il.text_colorize(line, textmatcher, allocated)

            print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
