#!/usr/bin/python

from __future__ import print_function

import sys
import time
import baseformat
import irccolor

notify_interval = 90

def blacklisted(channel, t, (l, p, nick), text):
    plain = ''.join(map(lambda c: c[0], irccolor.colorize(text))).strip()

    if plain == '':
        return channel + '.blank'

    return None

fonxes = {}

def register_fonx(bl):
    if bl not in fonxes:
        fonxes[bl] = 0
    fonxes[bl] += 1

def fonx_summary(fonxes):
    if not fonxes:
        return 'none fonxed'
    return ', '.join(map(lambda (x,y): x+' '+str(y), sorted(sorted(fonxes.items(), key=lambda x: x[0]), key=lambda x: x[1], reverse=True)))

def main():
    global fonxes

    try:
        fonx = open('/tmp/fonx', 'a')
        line = sys.stdin.readline()

        nextnotify = time.time() + notify_interval

        while line:
            r = baseformat.splitter.match(line)
            if r:
                channel = r.group(2)
                t    = r.group(3)
                name = baseformat.nameformat_strip(r.group(4))
                text = r.group(5)

                bl = blacklisted(channel, t, name, text)
                if bl == None:
                    print(line, end='')
                    sys.stdout.flush()
                else:
                    register_fonx(bl)
                    print(line, end='', file=fonx)
                    fonx.flush()

            else:
                print(line, end='')
                sys.stdout.flush()

            if time.time() > nextnotify:
                if fonxes:
                    print('fonx\t' + str(int(round(time.time() * 1000))) + '\tfonxed\t' + fonx_summary(fonxes))
                nextnotify = time.time() + notify_interval
                fonxes = {}

            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
