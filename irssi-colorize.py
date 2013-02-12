#!/usr/bin/python

from __future__ import print_function

import sys
import termcolor


# TODO: fill in the gaps
irssi_fgattrs = {
    '\x32': (False, 'green'),
    '\x33': (False, 'cyan'),
    '\x35': (False, 'magenta'),
    '\x38': (True,  'grey'),
    '\x39': (True,  'blue'),
    '\x3a': (True,  'green'),
    '\x3b': (True,  'cyan'),
    '\x3c': (True,  'red'),
    '\x3d': (True,  'magenta'),
    }

level_log = False
level_warn = True
level_error = True

if len(sys.argv) > 1:
    level_log = True

def log(x):
    if level_log:
        print(x, file=sys.stderr)

def warn(x):
    if level_warn:
        print(x, file=sys.stderr)

def error(x):
    if level_error:
        print(x, file=sys.stderr)

def newlook():
    return {'bold':False,'fg':None,'bg':None}

def lookeq(x, y):
    return (x['bold'] == y['bold']) and (x['fg'] == y['fg']) and (x['bg'] == y['bg'])

defaultlook = newlook()

def main():
    clearseq = '\x1b[0m'
    printingstate = newlook()
    curstate = newlook()
    state = 0
    buf = None

    try:
        line = sys.stdin.readline()
        while line:
            buf = []

            for c in line:

                if state == 0:
                    if c == '\x02':
                        curstate = curstate.copy()
                        curstate['bold'] = not curstate['bold']
                    elif c == '\x03':
                        log('got ETX')
                        state = 3
                    elif c == '\x04':
                        log('got EOT')
                        state = 1
                    elif c == '\x0f':
                        log('reset state')
                        curstate = newlook()
                    else:
                        log('got c: ' + c + ' (' + hex(ord(c)) + ')')
                        buf.append((c, curstate))

                elif state == 1:
                    if c == '\x63':
                        curstate = curstate.copy()
                        curstate['bold'] = not curstate['bold']
                        log('toggle bold, now ' + str(curstate['bold']))
                        state = 0
                    elif c == '\x65':
                        log('going crankmode')
                        # This type only lasts up to \n - doesn't reset colours properly
                        # I don't like this format
                        state = 4
                    elif c == '\x67':
                        log('reset state')
                        curstate = newlook()
                        state = 0
                    elif c == '\x69':
                        # not sure entirely what this one is
                        log('x69')
                        state = 0
                    else:
                        log('read fg attr: ' + c + ' (' + hex(ord(c)) + ')')

                        if c in irssi_fgattrs:
                            curstate = curstate.copy()
                            curstate['bold'] = irssi_fgattrs[c][0]
                            curstate['fg'] = irssi_fgattrs[c][1]
                        else:
                            warn('unknown at fg attr: ' + c + ' (' + hex(ord(c)) + ')')

                        state = 2

                elif state == 2:
                    log('read attr2: ' + c + ' (' + hex(ord(c)) + ')')
                    curstate = curstate.copy()

                    if c == '\x2f':
                        curstate['bg'] = None
                    else:
                        warn('unknown at bg attr: ' + c + ' (' + hex(ord(c)) + ')')

                    state = 0

                elif state == 3:
                    # It is impossible to correctly parse this type of color format.
                    # The format is TEXT ^C BYTE [BYTE] TEXT
                    # where byte can be a valid text char...
                    # The following are all cases I've seen where it
                    # was just one byte, I don't have time to write a
                    # fuzzy parser for multi bytes

                    curstate = curstate.copy()

                    if c == '\x33':
                        curstate['bold'] = False
                        curstate['fg'] = 'green'
                    elif c == '\x34':
                        curstate['bold'] = True
                        curstate['fg'] = 'red'
                    elif c == '\x37':
                        curstate['bold'] = False
                        curstate['fg'] = 'yellow'
                    else:
                        warn('unknown at bg attr: ' + c + ' (' + hex(ord(c)) + ')')

                    state = 0

                elif state == 4:
                    if c == '\x02':
                        curstate = curstate.copy()
                        curstate['bold'] = True
                        curstate['fg'] = None
                        curstate['bg'] = None
                        state = 0
                    elif c == '\x04':
                        # i've inserted some of these myself
                        log('got EOT')
                        state = 1
                    else:
                        log('got c: ' + c + ' (' + hex(ord(c)) + ')')
                        buf.append((c, curstate))
                        state = 0

                else:
                    error('unknown state: ' + str(state))

            for c in buf:
                if lookeq(printingstate, c[1]):
                    print(c[0], end='')
                else:
                    if (lookeq(c[1], defaultlook) or
                        (printingstate['bold'] and (not c[1]['bold'])) or
                        (printingstate['fg'] and (not c[1]['fg'])) or
                        (printingstate['bg'] and (not c[1]['bg']))):
                        print(clearseq, end='')

                    if printingstate['fg'] == c[1]['fg']:
                        fg = None
                    else:
                        fg = c[1]['fg']

                    if printingstate['bg'] == c[1]['bg']:
                        bg = None
                    else:
                        bg = c[1]['bg']

                    if (printingstate['bold'] == c[1]['bold']) or (not c[1]['bold']):
                        attrs = None
                    else:
                        attrs = []
                        attrs.append('bold')

                    printingstate = c[1]

                    # use [:-4] to remove the clear sequence
                    print(termcolor.colored(c[0], fg, bg, attrs)[:-4], end='')

                if c[0] == '\n':
                    # this is a bit overkill but there was at least one state that needed it
                    if not lookeq(curstate, defaultlook):
                        # if we hit newline c[1] == curstate by definition
                        print(clearseq, end='')
                        curstate = newlook()
                        printingstate = curstate

                    sys.stdout.flush()

            line = sys.stdin.readline()

    except KeyboardInterrupt:
        log('closing')

if __name__ == '__main__':
    main()
