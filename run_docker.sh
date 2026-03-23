#docker run -d --name my_scan portscan sleep infinity
#docker exec -it my_scan bash
#docker build -t port-scanner .
#docker run --rm --network host --cap-add=NET_RAW --cap-add=NET_ADMIN port-scanner

#docker run --rm -it --network host --cap-add=NET_RAW --cap-add=NET_ADMIN -v $(pwd):/app portscan /bin/bash

docker run --rm -it --network host --cap-add=NET_RAW --cap-add=NET_ADMIN -v $(pwd):/app portscan 



#masscan 192.168.1.1-192.168.1.255 --ping --rate 100 --wait 5 --retries 0 > <IPs>
#masscan <IPs> -p ports --rate 1000 --wait 5 --retries 0 > <Ports>
#nmap -sV <IPs> -p <Ports> > <Banners>
#response <Banners> exploit_db