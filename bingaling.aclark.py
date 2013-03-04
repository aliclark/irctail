#!/usr/bin/python

import re

import baseformat
import bingaling

bingcheck_restr = r'([a4][c][l1][a4][r][k])|([a4][l1][i1])'
bingcheck_full  = re.compile(r'(('+'\x04\x65'+r')|('+'\x04\x63'r')|([^\w\-'+'\x04'+r'])|(^)|(\t))(' + bingcheck_restr + r')(([^\w\-])|($))', re.IGNORECASE)

def bingcheck(line):
    r = baseformat.splitter.match(line)

    if r:
        sub = r.group(3) + '\t' + r.group(4) + '\t' + re.sub(bingcheck_full, '\\1\x16\\7\x16\\11', r.group(5));

        if r.group(1):
            sub = r.group(1) + sub
    else:
        sub = re.sub(bingcheck_full, '\x16\\7\x16', line);

    if sub != line:
        bingaling.sendmail('aclark@localhost', line)

    return sub

def main():
    bingaling.bingpipe(bingcheck)

if __name__ == '__main__':
    main()
