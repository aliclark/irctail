#!/usr/bin/python

from __future__ import print_function

import sys
import re
import datetime

stamp_format = '%H:%M:%S'

def stamp_to_time(x):
    x = int(x)
    return datetime.datetime.fromtimestamp(round(x / 1000.0)).strftime(stamp_format)

def main():
    reg = re.compile('^(\ *[^\ \t]+)([\ \t])(.*)')

    line = sys.stdin.readline()
    while line:
        r = reg.match(line)

        if r:
            line = stamp_to_time(r.group(1)) + r.group(2) + r.group(3) + '\n'

        print(line, end='')
        line = sys.stdin.readline()

if __name__ == '__main__':
    main()
