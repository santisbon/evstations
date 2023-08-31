FROM  debian
SHELL ["/bin/bash", "-c"]

RUN   apt update && apt upgrade -y \
      && apt install -y python3 pip \
      && pip3 install sseclient pika --break-system-packages
COPY  ./*.py /etc/watcher/
CMD   [ "python3", "/etc/watcher/watcher.py" ]
