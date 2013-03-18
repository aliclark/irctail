#!/usr/bin/python

from __future__ import print_function

import sys
import re
import baseformat

emailonly = re.compile(r'.*<(.*)>.*')
botonly   = re.compile(r'-(Bot):.*-')

def rename(x):
    prev = None
    while prev != x:
        prev = x
        x = x.replace('@example.net', '')
        x = re.sub(emailonly, '\\1', x)
        x = re.sub(botonly, '\\1', x)
    return x

def main():
    try:
        line = sys.stdin.readline()

        while line:
            r = baseformat.splitter.match(line)
            if r:
                print(r.group(1) + r.group(3) + '\t' + rename(r.group(4)) +
                      '\t' + r.group(5),
                      end='')
            else:
                print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
