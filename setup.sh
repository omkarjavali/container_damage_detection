#!/bin/bash

# Use a faster or more reliable Debian mirror
echo "Using deb.debian.org mirror"
sudo sed -i 's|http://deb.debian.org/debian|http://ftp.us.debian.org/debian|g' /etc/apt/sources.list

# Update package list
sudo apt-get update -y
