#!/bin/bash

dirformat="$HOME/irclogs/freenode"
outfile=/tmp/irssitail
onlythese=''

basestr=`date "+$dirformat"`

ps ux | grep tail >irctail-spawn.pslist

for x in `ls $basestr`; do
    if [ "$onlythese" == '' ] || [[ "$onlythese" == *"$x"* ]]; then
        if [ -e $basestr/$x ] && ! grep -E "$basestr/$x\$" irctail-spawn.pslist >/dev/null ; then
            echo "$basestr/$x"
            tailf $basestr/$x | sed -u "s/^/`echo $x | sed 's/\.log//'`\t/" >>$outfile &
        fi
    fi
done

