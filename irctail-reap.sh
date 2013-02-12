#!/bin/bash

thisdate="`date '+%Y/%m/%d'`"

if [ "$1" == 'all' ]; then
    thisdate='oajfoj3983a3' # reap everything
fi

for pid in `ps ux | grep 'tail' | grep -v $thisdate | grep log | awk '{ print $2 }'`; do
    kill $pid
done
