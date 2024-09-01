
# docker build . -t haproxy-dashboard --progress=plain  --no-cache
FROM docker.io/debian:bookworm

RUN set -Eeuo; \
    # update the system \
    apt-get update && \
    # install packages \
    apt-get install -y --no-install-recommends python3-pip build-essential && \
    # clean the package cache \
    apt-get clean && \
    # clean cache \
    rm -rf /var/lib/apt/lists/* && \
    # fix error: externally-managed-environment error \
    rm /usr/lib/python3*/EXTERNALLY-MANAGED

COPY . /tmp/haproxy-configurator

RUN set -Eeuo; \
    # Create the folder inside /etc
    cd /tmp/haproxy-configurator && \
    mkdir -p /etc/haproxy-configurator/templates && \
    # Copy files to the 'haproxy-configurator' folder \
    cp -r templates/* /etc/haproxy-configurator/templates/ && \
    cp app.py /etc/haproxy-configurator/ && \
    cp Makefile /etc/haproxy-configurator/ && \
    cp requirements.txt /etc/haproxy-configurator/ && \
    cp ssl.ini /etc/haproxy-configurator/ && \
    cp -r ssl/ /etc/haproxy-configurator/ && \
    # Remove temporary directory \
    rm -rf /tmp/haproxy-configurator && \
    cd /etc/haproxy-configurator/ && \
    # Install dependencies \
    make install && \
    # Create the haproxy directory \
    mkdir -p /etc/haproxy && \
    # create an empty haproxy config file \
    touch /etc/haproxy/haproxy.cfg

EXPOSE 5000

CMD [ "/usr/bin/python3", "/etc/haproxy-configurator/app.py" ]