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
                      '\t' + r.group(5))
            else:
                print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
