#!/bin/bash

# Create the folder inside /etc
sudo mkdir -p /etc/haproxy-configurator

# Copy files to the 'haproxy-configurator' folder

sudo cp -r templates/ /etc/haproxy-configurator/
sudo cp app.py /etc/haproxy-configurator/
sudo cp Makefile /etc/haproxy-configurator/
sudo cp requirements.txt /etc/haproxy-configurator/
sudo cp ssl.ini /etc/haproxy-configurator/
sudo cp -r ssl/ /etc/haproxy-configurator/


# Create the service file for 'haproxy-configurator'
cat << EOF | sudo tee /etc/systemd/system/haproxy-configurator.service
[Unit]
Description=Haproxy-Configurator Service By Alon Zur

[Service]
ExecStart=/usr/bin/python3 /etc/haproxy-configurator/app.py
Restart=always
RestartSec=3
StandardOutput=/var/log/haproxy-configurator_std_output.log
StandardError=/var/log/haproxy-configurator_error.log
[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to load the new service
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable haproxy-configurator.service
sudo systemctl start haproxy-configurator.service
