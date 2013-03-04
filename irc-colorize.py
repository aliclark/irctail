#!/usr/bin/python

from __future__ import print_function

import sys
import termcolor_1_1_0 as termcolor

# Good resource for ANSI escapes:
# http://wiki.bash-hackers.org/scripting/terminalcodes
# Good resource for mIRC colors:
# http://www.mirc.com/colors.html

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
    return {'bold':False,'reverse':False,'fg':None,'bg':None}

def lookeq(x, y):
    return (x['bold'] == y['bold']) and (x['reverse'] == y['reverse']) and (x['fg'] == y['fg']) and (x['bg'] == y['bg'])

defaultlook = newlook()

# I think this model of color is incorrect,
# the bold colours are only coincidentally bold,
# a toggle should not turn boldness off i think
mirc_colors = [
    ('white', True),
    ('grey', None),
    ('blue', None),
    ('green', None),
    ('red', True),
    ('red', None),
    ('magenta', None),
    ('yellow', None),
    ('yellow', True),
    ('green', True),
    ('cyan', None),
    ('cyan', True),
    ('blue', True),
    ('magenta', True),
    ('grey', True),
    ('white', None),
    ]

def parsefg(s):
    if ',' in s:
        s = s[:s.index(',')]
    n = int(''.join(s))
    if n > 15:
        log('crank mirc: ' + str(n))
        # no idea where these came from
        if n == 21:
            return ('red', False)
        elif n == 25:
            return ('green', True)
        return None
    return mirc_colors[n]

def parsebg(s):
    return parsefg(s[s.index(',')+1:])

def main():
    clearseq = '\x1b[0m'
    printingstate = newlook()
    curstate = newlook()

    state = 0
    buf = None
    s3 = None

    try:
        line = sys.stdin.readline()
        while line:
            buf = []

            for c in line:
                # allows reinterpreting the character in a different state
                while True:
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
                        elif c == '\x13':
                            log('strikethrough not implemented')
                        elif c == '\x15':
                            log('underline not implemented')
                            # '\x1b[0;4m'
                        elif c == '\x16':
                            curstate = curstate.copy()
                            curstate['reverse'] = not curstate['reverse']
                        elif c == '\x1f':
                            # same as underline?
                            # '\x1b[0;4m'
                            log('underline2 not implemented')
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

                        if c == '\x2f':
                            curstate = curstate.copy()
                            curstate['bg'] = None
                        else:
                            warn('unknown at bg attr: ' + c + ' (' + hex(ord(c)) + ')')

                        state = 0

                    elif state == 3:
                        # format is \x03N[,M]
                        # at this point we've already received \x03
                        # eg.
                        # 1     (foreground black)
                        # 10    (foreground cyan)
                        # 1,2   (foreground black, background darkblue)
                        # 1,10  (foreground black, background cyan)
                        # 10,13 (foreground cyan, background violet)
                        # 10,99 (foreground cyan, background transparent)

                        s3 = []
                        if c.isdigit():
                            s3.append(c)
                            state = 5
                        else:
                            # "A plain ^C can be used to turn off all
                            # previous color attributes."
                            # Here I take that to mean color attributes
                            # set by *any* method, not just ^C
                            curstate = curstate.copy()
                            curstate['fg'] = None
                            curstate['bg'] = None
                            state = 0
                            continue

                    elif state == 4:
                        if c == '\x02':
                            curstate = curstate.copy()
                            curstate['bold'] = True
                            curstate['fg'] = None
                            curstate['bg'] = None
                            state = 0
                        elif c == '\x03':
                            # i've inserted some of these myself
                            log('got EOT')
                            state = 3
                        else:
                            # anything else just gets reinterpreted
                            state = 0
                            continue

                    elif state == 5:
                        if c.isdigit():
                            s3.append(c)
                            state = 6
                        elif c == ',':
                            s3.append(c)
                            state = 7
                        else:
                            curstate = curstate.copy()
                            tmpx = parsefg(s3)
                            curstate['fg'] = tmpx[0]
                            curstate['bold'] = tmpx[1] if tmpx[1] else curstate['bold']
                            state = 0
                            continue

                    elif state == 6:
                        if c == ',':
                            # if the bg part turns out to be bogus, we'll
                            # still want to print the comma
                            s3.append(c)
                            state = 7
                        else:
                            # time to print using the new foreground
                            curstate = curstate.copy()
                            tmpx = parsefg(s3)
                            curstate['fg'] = tmpx[0]
                            curstate['bold'] = tmpx[1] if tmpx[1] else curstate['bold']
                            state = 0
                            continue

                    # start parseing background
                    elif state == 7:
                        if c.isdigit():
                            # full sequence is now considered "valid"
                            s3.append(c)
                            state = 8
                        else:
                            # the comma must have been text
                            curstate = curstate.copy()
                            tmpx = parsefg(s3[:-1])
                            curstate['fg'] = tmpx[0]
                            curstate['bold'] = tmpx[1] if tmpx[1] else curstate['bold']
                            buf.append((s3[-1], curstate))
                            state = 0
                            continue

                    elif state == 8:
                        if c.isdigit():
                            s3.append(c)
                            curstate = curstate.copy()
                            tmpx = parsefg(s3)
                            curstate['fg'] = tmpx[0]
                            curstate['bold'] = tmpx[1] if tmpx[1] else curstate['bold']
                            # TODO: can we involve "dark" on bg?
                            tmpx = parsebg(s3)
                            if tmpx:
                                curstate['bg'] = tmpx[0]
                            else:
                                curstate['bg'] = None
                            state = 0
                        else:
                            curstate = curstate.copy()
                            tmpx = parsefg(s3)
                            curstate['fg'] = tmpx[0]
                            curstate['bold'] = tmpx[1] if tmpx[1] else curstate['bold']
                            # TODO: can we involve "dark" on bg?
                            tmpx = parsebg(s3)
                            if tmpx:
                                curstate['bg'] = tmpx[0]
                            else:
                                curstate['bg'] = None
                            state = 0
                            continue

                    else:
                        error('unknown state: ' + str(state))

                    break

            for c in buf:
                if lookeq(printingstate, c[1]):
                    print(c[0], end='')
                else:
                    if (lookeq(c[1], defaultlook) or
                        (printingstate['bold'] and (not c[1]['bold'])) or
                        (printingstate['reverse'] and (not c[1]['reverse'])) or
                        (printingstate['fg'] and (not c[1]['fg'])) or
                        (printingstate['bg'] and (not c[1]['bg']))):
                        print(clearseq, end='')

                    if printingstate['fg'] == c[1]['fg']:
                        fg = None
                    else:
                        fg = c[1]['fg']

                    if (not c[1]['bg']) or (printingstate['bg'] == c[1]['bg']):
                        bg = None
                    else:
                        bg = 'on_' + c[1]['bg']

                    attrs = None

                    if not ((printingstate['bold'] == c[1]['bold']) or (not c[1]['bold'])):
                        if not attrs:
                            attrs = []
                        attrs.append('bold')

                    if not ((printingstate['reverse'] == c[1]['reverse']) or (not c[1]['reverse'])):
                        if not attrs:
                            attrs = []
                        attrs.append('reverse')

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
