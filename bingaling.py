#!/usr/bin/python

from __future__ import print_function

import sys
import subprocess
import datetime

import baseformat
import irccolor

# There are multiple purposes of this program:

# * To make sure that I address or am aware each and every mention of
#   me, in case I need to say anything.
#   Irssi does highlight channels, but could still miss an earlier bing
#   if there are multiple and I only check the most recent.
#   For this, mail would be a good fit.

# * To provide a more visible alert system when attention is
#   needed. It shouldn't be necessary to watch IRC *all* of the time, or
#   even frequently - this would detract from programming or other
#   tasks.
#   Instead, it should be fine to miss most of the chat for 30mins to an
#   hour at a time, yet be alerted when there is a problem.
#   For this, any of bubble notificaion, SMS, or mail (provided the
#   unread mail is noticeable) would be a good fit.

# TODO: it would be really cool if I can hit reply and have each line
# of response go to the correct channel, with the user's nick
# prepended.
#
# First I'd have to learn how to write an IRC inserter (making it
# appear as my own nick)
#
# Then I'd have to actually be sending it to myself at something like
# ~/mail/sendirc, where a script would look for any new messages
# coming into the folder and send off an IRC message.
#
def sendmail(to, text):
    xtra = ''
    r = baseformat.splitter.match(text)

    if r:
        fromstr = 'sendirc@localhost'
        channel = r.group(2)
        time = baseformat.timeformat(r.group(3))
        user = r.group(4)
        rest = r.group(5)

        dt = datetime.datetime.fromtimestamp(int(r.group(3)[:-3]))
        xtra += 'Date: ' + dt.strftime('%a, %d %b %Y %H:%M:%S %z') + '\n'

        (leadstr, uperm, nick) = baseformat.nameformat_strip(user)
        xtra += 'X-BingFrom: ' + nick + '\n'

        if leadstr:
            userstr = leadstr + uperm + nick
        else:
            userstr = '<' + uperm + nick + '>'

        if channel:
            xtra += 'X-BingChan: ' + channel + '\n'

        subj = baseformat.combine_parts(channel, time, userstr, rest)
        body = userstr + ' ' + rest

    else:
        fromstr = 'noreply@localhost'
        subj = text
        body = text

    plainsubj = ''.join(map(lambda c: c[0], irccolor.colorize(subj)))
    plainbody = ''.join(map(lambda c: c[0], irccolor.colorize(body)))

    # TODO: use a Python library for sending
    ch = subprocess.Popen(['sendmail', to], stdin=subprocess.PIPE)

    full = ('To: ' + to + '\n' +
'From: ' + fromstr + '\n' +
'Subject: ' + plainsubj +
xtra +
'\n' +
plainbody)

    ch.stdin.write(full)

    ch.stdin.close()
    ch.wait()

# In fact, I think I'll have the filter before this program, so that
# any lines that reach this point *will* perform a binging action.
#
# However, if the text is to be *modified* by this program, then I'll
# need to separate the bing stream from the non-bing stream and
# re-merge it after modification. This would require something like a
# "grepsplit" program, which takes a regex as its argument, and
# outputs to two files, with filenames given as arguments 2 and 3.

def bingpipe(bingcheck):
    try:
        line = sys.stdin.readline()

        while line:
            print(bingcheck(line), end='')
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

def nothing(line):
    return line

def main():
    bingpipe(nothing)

if __name__ == '__main__':
    main()
