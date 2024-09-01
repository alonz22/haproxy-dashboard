
FROM docker.io/debian:bookworm

# docker run -it  docker.io/debian /bin/bash
RUN <<EOF
    apt-get update &&                                               # update the system
    apt-get install -y --no-install-recommends python3-pip &&
    rm -rf /var/lib/apt/lists/* &&                                  # clean cache
    rm /usr/lib/python3*/EXTERNALLY-MANAGED                         # fix error: externally-managed-environment error
EOF
COPY . /tmp/haproxy-configurator

RUN cd /tmp/haproxy-configurator; \
    # Create the folder inside /etc \
    mkdir -p /etc/haproxy-configurator/templates; \
    # Copy files to the 'haproxy-configurator' folder \
    cp -r templates/* /etc/haproxy-configurator/templates/ && \
    cp app.py /etc/haproxy-configurator/ && \
    cp Makefile /etc/haproxy-configurator/ && \
    cp requirements.txt /etc/haproxy-configurator/ && \
    cp ssl.ini /etc/haproxy-configurator/ && \
    cp -r ssl/ /etc/haproxy-configurator/; \
    # Remove tmp folder \
    rm -rf /tmp/haproxy-configurator; \
    # Install dependencies \
    cd /etc/haproxy-configurator/ && \
    make install; \
    # Create an empty haproxy folder \
    mkdir -p /etc/haproxy && \
    touch /etc/haproxy/haproxy.cfg

EXPOSE 5000

CMD [ "/usr/bin/python3", "/etc/haproxy-configurator/app.py" ]