
# private
pallette = {'grey': '\x38', 'blue': '\x39', 'green': '\x3a', 'cyan': '\x3b', 'red': '\x3c', 'magenta': '\x3d'}

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
    return '\x04' + pallette[c] + '\x2f'

def pick_color(counts, hits):
    minc = None
    minn = None
    minh = None

    for (k,v) in counts.items():
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

        if ((minn == None) or (v < minn) or
            ((v == minn) and (minh != None) and ((ch(k) not in hits) or (hits[ch(k)] < minh)))):
            minc = k
            minn = v
            if ch(k) in hits:
                minh = hits[ch(k)]
            else:
                minh = None

    counts[minc] += 1
    return ch(minc)

def getcolor(s, allocated, counts, hits):
    if s not in allocated:
        allocated[s] = pick_color(counts, hits)
    return allocated[s]
