#!/bin/bash

# create the vision log file if it doesn't exist
touch /var/log/vision.log

# change ownership of the file

# make sure we have write permissions on the file
chmod 666 /var/log/vision.log

# set static address on eth0 (.13 for vision)
sudo cat dhcpcd-changes >> /etc/dhcpcd.conf

