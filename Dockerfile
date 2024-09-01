
# docker build . -t haproxy-dashboard --progress=plain  --no-cache
FROM docker.io/python:bookworm

RUN echo "Update system and install dependencies" && \ 
    # update the system \
    apt-get update && \
    # install packages \
    apt-get install -y --no-install-recommends python3-pip haproxy && \
    # clean the package cache \
    apt-get clean && \
    # clean cache \
    rm -rf /var/lib/apt/lists/*

        
ARG USERNAME=haproxy-dashboard
ARG USER_UID=1001

# Create the user
RUN useradd --uid $USER_UID --gid 0 -m $USERNAME

# Use build --no-cache if change it
COPY --chown=$USERNAME:0 . /etc/haproxy-configurator
WORKDIR /etc/haproxy-configurator


# Create the haproxy directory and config file \
RUN mkdir -p /etc/haproxy && \
    touch /etc/haproxy/haproxy.cfg && \
    # Give the permission to haproxy \
    chmod g=u /etc/haproxy/haproxy.cfg


# Switch to user
USER $USERNAME

# Create a virtual environment named and install dependencies
RUN python -m pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "/etc/haproxy-configurator/app.py" ]