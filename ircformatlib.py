
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

import re

# TODO: allow a list of colours we shouldn't use for highlighting,
# because they would normally clash on the background colour
forbidden = []

# private
pallette = {'white': '00', 'blue': '12', 'green': '09', 'cyan': '11', 'red': '04', 'magenta': '13', 'yellow': '08', 'grey': '14'}

clearseq = '\x04\x67'

# private
crankseq = '\x04\x65'

def getmaxlen(s, maxlen):
    if len(s) > maxlen:
        return len(s)
    return maxlen

def getmaxpad(s, maxlen):
    return ((maxlen - len(s)) * ' ')

def uplogs(color, hits):
    if color not in hits:
        hits[color] = 0
    hits[color] += 1

# private
def ch(c):
    return '\x03' + pallette[c] + ',99'

# TODO: use only minimal sequences necessary
# ^Cf  if the name starts with a non-digit, non-comma character (and fg
#      is <10) or the comma is followed by a non-digit
# ^Cff if the name starts with a non-comma character or the comma is
#      followed by a non-digit
# ^Cff,99 otherwise

def pick_color(name, allocated, counts, hits):
    l = len(name)

    minc = None
    minn = None
    minh = None
    minl = None

    ds = {}

    for k in pallette.keys():
        ds[ch(k)] = -1

    for k,v in allocated.items():
        kl = abs(len(k) - l)
        if (ds[v] == -1) or (ds[v] > kl):
            ds[v] = kl

    for (k, v) in [(k, counts[k] if k in counts else 0) for k in pallette.keys()]:
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
        #
        # TODO: This will fall back to aggregate counts if all colors
        # have already allocated an item with same string length -
        # this is sub-optimal, should be using per color, per string
        # length counts

        if ((ds[ch(k)] == -1) or ((minl != -1) and (ds[ch(k)] > minl)) or
            ((ds[ch(k)] == minl) and
             ((minn == None) or (v < minn) or
              ((v == minn) and (minh != None) and
               ((ch(k) not in hits) or (hits[ch(k)] < minh)))))):
            minc = k
            minn = v
            minl = ds[ch(k)]
            if ch(k) in hits:
                minh = hits[ch(k)]
            else:
                minh = None

    if not minc in counts:
        counts[minc] = 0

    counts[minc] += 1
    return ch(minc)

def getcolor(s, allocated, counts, hits):
    if s not in allocated:
        allocated[s] = pick_color(s, allocated, counts, hits)
    return allocated[s]

# NOTE: this function could do with optimisation - it takes up
# increasingly more CPU after a day of 30 busy channels - presumably
# because of the regexp text replace on so many usernames.
#
# Potentially set a limit on the items in "allocated" to replace for,
# so that once the limit is reached we are no longer replacing all
# names. This would need to adapt if a given user starts posting
# again.
#
# Either:
# 1) only bump the counter when a user is referenced
# 2) bump counter when user posts a message
# 3) some combination of the above
#
# It is much cheaper to just do (2), and should still be quite
# accurate.

# XXX: Quite annoying but potentially difficult to solve is that if
# the name appears in an already colored sequence, the original color
# will be cleared by the clearseq, as well as the name's colour
#
# Would need to parse backwards for an existing color to do this
# right, or implement a push/pop control sequence

def text_colorize(after, textmatcher, allocated):
    for u,c in allocated.items():
        if u not in textmatcher:
            # Make any preceding "#" characters optional in
            # colorizing, since we most likely want to associate the
            # channel name as a normal work with the full channel name
            for i in xrange(len(u)):
                if u[i] != '#':
                    break
            srch = re.escape(u)
            if (len(u[0]) > 0) and (u[0] == '#'):
                srch = '(' + srch[0:i*2] + ')?' + srch[i*2:]
            textmatcher[u] = re.compile(r'((' + crankseq + r')|('+'\x04\x63'r')|([^\w\-'+'\x04'+r'])|(^))(' + srch + r')(([^\w\-])|($))', re.IGNORECASE)

        after = re.sub(textmatcher[u], '\\1' + c + '\\6' + clearseq + '\\8', after)

    return after
