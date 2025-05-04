#!/bin/bash

# Use faster mirror (optional)
sudo sed -i 's|http://deb.debian.org|http://ftp.us.debian.org|g' /etc/apt/sources.list

# Retry update and install logic
RETRIES=5
COUNT=0
until [ $COUNT -ge $RETRIES ]
do
  sudo apt-get update -y && sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 && break
  COUNT=$((COUNT+1))
  echo "Retrying apt install... attempt $COUNT"
  sleep 5
done
