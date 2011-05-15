#!/bin/bash
torrentid=$1
torrentname=$2
torrentpath=$3

subject="Torrent Added"
message="$torrentname"

if test -z "$2"
then
    echo "Usage: notifyxbmc \"message\""
else
    xbmc-send -a "Notification($subject,$message)"
fi
