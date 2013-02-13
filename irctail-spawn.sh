#!/bin/bash

dirformat="$HOME/irclogs/freenode"
outfile=/tmp/irssitail
onlythese=''

basestr=`date "+$dirformat"`

# TODO: save results of ps aux | grep tail somewhere!

for x in `ls $basestr`; do
    if [ "$onlythese" == '' ] || [[ "$onlythese" == *"$x"* ]]; then
        if [ -e $basestr/$x ] && ! ps ux | grep tail | grep -E "$basestr/$x\$" >/dev/null ; then
            echo "$basestr/$x"
            tailf $basestr/$x | sed -u "s/^/`echo $x | sed 's/\.log//'`\t/" >>$outfile &
        fi
    fi
done
