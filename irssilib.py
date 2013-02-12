
import re

# private
pallette = {'white': '00', 'blue': '10', 'green': '09', 'cyan': '11', 'red': '04', 'magenta': '13', 'yellow': '08', 'grey': '14'}

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

def pick_color(counts, hits):
    minc = None
    minn = None
    minh = None

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

        if ((minn == None) or (v < minn) or
            ((v == minn) and (minh != None) and ((ch(k) not in hits) or (hits[ch(k)] < minh)))):
            minc = k
            minn = v
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
        allocated[s] = pick_color(counts, hits)
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

def text_colorize(after, textmatcher, allocated):
    for u,c in allocated.items():
        if u not in textmatcher:
            textmatcher[u] = re.compile('((' + crankseq + ')|([^\w\-])|(^))(' + re.escape(u) + ')(([^\w\-])|($))', re.IGNORECASE)

        after = re.sub(textmatcher[u], '\\1' + c + '\\5' + clearseq + '\\6', after)

    return after
