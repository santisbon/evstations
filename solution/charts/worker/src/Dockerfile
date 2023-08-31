FROM  debian
SHELL ["/bin/bash", "-c"]

RUN   apt update && apt upgrade -y \
      && apt install -y python3 pip \
      && pip3 install pika geopy urllib3 tabulate redis --break-system-packages
COPY  ./*.py /etc/worker/
CMD   [ "python3", "/etc/worker/worker.py" ]
