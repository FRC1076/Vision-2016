#!/bin/bash
#
# Only start up the driver cam if it is not already running.
#
# Check if there is a process called mjpg_streamer.  If there
# is, then we'll just print a helpful message for the user.
#
if [[ $(pidof mjpg_streamer) ]];
then
    echo "mjpg_streamer is already streaming!";
    echo "View stream at: http://$HOSTNAME:8001/?action=stream";
else
    echo "mjpg_streamer is *NOT YET* running, so we'll start it up!";
    cd /usr/src/mjpg-streamer/mjpg-streamer-experimental
    ./driver-video.sh
fi
