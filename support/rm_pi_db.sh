#!/bin/bash

sudo service pihole-FTL stop
sudo rm /etc/pihole/pihole-FTL.db
sudo service pihole-FTL start
