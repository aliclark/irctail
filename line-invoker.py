#!/usr/bin/python

from __future__ import print_function

import sys
import subprocess

# A normal(ish) pipeline looks like the following:
# tailf input | grep -v foo | grep bar | cat >>output

# If we want to change the valu "foo", "bar" or otherwise change the
# pipeline, we have to kill the old pipeline and start a new one.

# This script changes the above to
# tailf input | line-invoker.py mypipeline.sh | cat >>output

# where mypipeline.sh contains:
# grep -v foo | grep bar

# This allows the pipeline to be edited at will, without breaking the
# tailf and potentially having missed lines, or duplicated them on
# restarting tailf

def main():
    prog = sys.argv[1]
    try:
        line = sys.stdin.readline()
        while line:
            p = subprocess.Popen(prog, stdin=subprocess.PIPE)
            p.stdin.write(line)
            p.stdin.close()
            sys.stdout.flush()
            line = sys.stdin.readline()

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
