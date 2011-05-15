#! /bin/bash

if test -z "$1"
then
    echo "Usage: notifyxbmc \"message\""
else
    xbmc-send -a "Notification(xbmc:,$1)"
fi
