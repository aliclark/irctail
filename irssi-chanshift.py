#!/usr/bin/python

from __future__ import print_function

import sys
import re

def main():
    m = re.compile('^(\ *[^\ ]+)([\ \t])(\d\d:\d\d:\d\d)(.*)')
    try:
        line = sys.stdin.readline()
        while line:
            print(re.sub(m, '\\3\\2\\1\\4', line), end='')
            sys.stdout.flush()
            line = sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
