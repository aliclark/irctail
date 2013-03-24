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
import datetime
import ircformatlib as il

# Allow this to be supplied as an option?
timeformat_format = '%H:%M:%S'
timeformat_filler = ' ' * len(datetime.datetime.now().strftime(timeformat_format))

def timeformat(time):
    try:
        x = int(time)
        dt = datetime.datetime.fromtimestamp(round(x / 1000.0))
        return dt.strftime(timeformat_format)
    except:
        return timeformat_filler

def colorized_newstate():
    return { 'maxlen': 0, 'hits': {}, 'counts': {}, 'allocated': {},
             'textmatcher': {} }

def colorized_text(state, text, leadstr=''):
    state['maxlen'] = il.getmaxlen(leadstr + text, state['maxlen'])
    color = il.getcolor(text, state['allocated'], state['counts'],
                        state['hits'])
    il.uplogs(color, state['hits'])
    return (il.getmaxpad(leadstr + text, state['maxlen']) + leadstr +
            color + text + il.clearseq)

chanformat_state = colorized_newstate()

def chanformat(channel):
    if not channel:
        return ''
    return colorized_text(chanformat_state, channel)

nameformat_state = colorized_newstate()

def nameformat_strip(name):
    leadstr = ''
    uperm = ''

    for lead in ('--- ', '* '):
        if name.startswith(lead):
            leadstr = lead
            name = name[len(lead):]
            break

    for perm in ('@', '+', '%', '*'):
        if name.startswith(perm):
            uperm = perm
            name = name[len(perm):]
            break

    return (leadstr, uperm, name)

def nameformat(name):
    (leadstr, uperm, name) = nameformat_strip(name)
    return colorized_text(nameformat_state, name, leadstr + uperm)

def textformat(text):
    return il.text_colorize(il.text_colorize(text,
                                             chanformat_state['textmatcher'],
                                             chanformat_state['allocated']),
                            nameformat_state['textmatcher'],
                            nameformat_state['allocated'])

def combine_parts(channel, time, name, text):
    tcsep = ''
    if time and channel:
        tcsep = ' '
    if not channel:
        channel = ''
    return time + tcsep + channel + ' ' + name + ' ' + text

splitter = re.compile(r'(([^\t]+)\t)?([^\t]+)\t([^\t]+)\t([^\t]+)')

def main():
    try:
        line = sys.stdin.readline()

        while line:
            r = splitter.match(line)

            if r:
                line = combine_parts(chanformat(r.group(2)),
                                     timeformat(r.group(3)),
                                     nameformat(r.group(4)),
                                     textformat(r.group(5)))
            else:
                line = textformat(line)

            print(line, end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
