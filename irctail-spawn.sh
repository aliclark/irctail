#!/bin/bash

dirformat="$HOME/irclogs/freenode"
outfile=/tmp/irssitail
onlythese=''

basestr=`date "+$dirformat"`

for x in `ls $basestr`; do
    if [ "$onlythese" == '' ] || [[ "$onlythese" == *"$x"* ]]; then
        if [ -e $basestr/$x ] && ! ps ux | grep tailf | grep $basestr/$x >/dev/null ; then
            tailf $basestr/$x | sed -u "s/^/`echo $x | sed 's/\.log//'`\t/" >>$outfile &
        fi
    fi
done
