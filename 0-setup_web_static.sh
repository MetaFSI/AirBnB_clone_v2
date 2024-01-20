#!/usr/bin/env bash
# Bash script for setting up web servers for the deployment of web_static

# Update package list
apt-get -y update > /dev/null

# Install nginx
apt-get install -y nginx > /dev/null

# Create necessary directories and file
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
touch /data/web_static/releases/test/index.html
echo "Hello World again!" > /data/web_static/releases/test/index.html

# Check if the 'current' directory exists and remove it
if [ -d "/data/web_static/current" ]; then
    sudo rm -rf /data/web_static/current
fi

# Create a symbolic link to 'test'
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership to user 'ubuntu'
chown -R ubuntu:ubuntu /data

# Configure nginx to serve content pointed to by symbolic link to hbnb_static
sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart nginx server
service nginx restart
