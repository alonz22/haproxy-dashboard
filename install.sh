#!/bin/bash

# Create the folder 'simplelb' inside /etc
sudo mkdir -p /etc/haproxy-configurator

# Copy 'config.ini' to the 'simplelb' folder
sudo cp -r templates/ /etc/haproxy-configurator/
sudo cp app.py /etc/haproxy-configurator/


# Create the service file for 'simplelb' (Assuming you want a systemd service)
cat << EOF | sudo tee /etc/systemd/system/haproxy-configurator.service
[Unit]
Description=Simple Load Balancer Service By Alon Zur

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

# Enable and start the 'simplelb' service
sudo systemctl enable haproxy-configurator.service
sudo systemctl start haproxy-configurator.service