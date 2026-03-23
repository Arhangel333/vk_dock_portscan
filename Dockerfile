
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    masscan \ 
    nmap \           
    python3 \           
    python3-pip \       
    libpcap-dev

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY . /app

RUN mkdir -p /app/results /app/logs

CMD ["python3", "main.py"]