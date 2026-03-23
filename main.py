import subprocess
import json
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


Token = config['masscan']['Token']
Outfile1 = config['masscan']['Outfile1']
Outfile2 = config['masscan']['Outfile2']
History_file = config['masscan']['History_file']
IPs = config['masscan']['IPs']
Ports = config['masscan']['Ports']
Rate = config['masscan']['Rate']
Ad_flags = config['masscan']['Ad_flags']
Ping = config['masscan']['Ping']

fullwork = 1 #0 - не работаем 1+ - работаем
verbose = 1

def check_history(history, cash):
    if not cash:
        print("В текущем сканировании не найдено открытых портов")
        return set(), set()
        
    cash_keys = set()
    for ip in cash:
        for port in ip['ports']:
            cash_keys.add(f"{ip['ip']}:{port['port']}")

    if not history:
        print("История пуста")
        new_ports = cash_keys
        closed_ports = set()
        return new_ports, closed_ports
    
    
    
    history_keys = set(history.keys())
    
    cash_ips = set()
    for key in cash_keys:
        ip = key.split(':')[0]
        cash_ips.add(ip)
    
    new_ports = cash_keys - history_keys
    
    closed_ports = set()
    
    for key in history_keys:
        ip = key.split(':')[0]
        if ip in cash_ips:
            if key not in cash_keys:
                
                closed_ports.add(key)
    
    if new_ports and verbose:
        print(f"Новых портов: {len(new_ports)}")
    if closed_ports and verbose:
        print(f"Закрывшихся портов: {len(closed_ports)}")
    
    return new_ports, closed_ports

ans = input(f"Использовать IP по умолчанию?(IP={IPs})\n(y/n)")
if ans != "y":
    ip = input("Введите IP (например, 192.168.1.1-192.168.1.255): ")
    print(f"ips : {ip}")
else:
    ip = IPs

ans = 0

ans = input(f"Использовать порты по умолчанию?(ports={Ports})\n(y/n)")
if ans != "y":
    ports = input("Введите порты (например, 80,443,8000-9000): ")
else:
    ports = Ports


ans = input(f"Использовать скорость по умолчанию?(rate={Rate})\n(y/n)")
if ans != "y":
    rate = input("Введите скорость (например, 100): ")
else:
    rate = Rate

ans1 = input(f"Использовать ping-разведку для обнаружения живых хостов?\n(y/n)")
if ans1 == "y":
    print(f"Получены параметры: ip = {ip}, ports = {ports}, rate = {rate}\n Начинаю разведку результаты будут записаны в файл {Outfile1}")
    if fullwork:
        subprocess.run(f"masscan {Ping} --retries 0 {ip} --rate {rate} -oJ {Outfile1}", shell=True)
    with open(Outfile1, "r") as f1:
        data = json.load(f1)
        ip = set()
        for el in data:
            ip.add(el['ip'])
    ip = ' '.join(ip)



first_comm = f"masscan {ip} -p{ports} --rate {rate} {Ad_flags} -oJ {Outfile2}"

if verbose:
    print(f"Получены параметры: ip = {ip}, ports = {ports}, rate = {rate}")
    print(f"Будет выполнено")
    print(first_comm)

if fullwork:
    result_masscan = subprocess.run(first_comm, shell=True)

print("masscan res: ", result_masscan)





try:
    with open(History_file, "r") as hf:
        history = json.load(hf)
except (FileNotFoundError, json.JSONDecodeError):
    print("Файл истории не найден или поврежден, создаем новый")
    history = {}

try:
    with open(Outfile2, "r") as cash_file:
        cash = json.load(cash_file)
except (FileNotFoundError, json.JSONDecodeError):
    print("Файл с результатами сканирования не найден или поврежден!")
    exit(1)




msg, closed = check_history(history, cash)


if verbose:
    print(msg)
    print(closed)
    print("#####"*10)
    for i in history:
        print(f"history : {i}")
    print("#####"*10)


for l in msg:
    adr = l.split(":")
    print(f"new : {l}")
    history[l] = {"ip": adr[0], "port": adr[1]}


for bastrd in closed:
    print(f"old : {bastrd}")
    del history[bastrd]

if verbose:
    print(closed)
    print("#####"*10)
    for i in history:
        print(f"history : {i}")
    print("#####"*10)



with open(History_file, "w") as story:
    try:
        json.dump(history, story, indent = '\t', sort_keys=True)
    except Exception as e:
        print(e)




#Send alert to vk

















class bot:
    url = "https://api.vk.com/method"
    token = config['vk']['token']
    version = config['vk']['version_api']

    def method(self, method, params):
        response = requests.get(f"{self.url}/{method}/", params=params)
        return response

class user:
    def __init__(self, user_id=None, name=None):
        self.id = user_id
        self.name = name


if msg:
    my_bot = bot()
    u = user()
    params = {
            'access_token': my_bot.token,
            'screen_name': config['vk']['name'],
            'v': my_bot.version
            }

    res = my_bot.method("utils.resolveScreenName", params)
    u.id = res.json()['response']['object_id']

    print(u.id)

    params = {
            'access_token': my_bot.token,
            'user_id': u.id,
            'random_id': 0,
            'v': my_bot.version, 
            'message' : f"Hello vk!\nNew ports have been scaned!\n"
            }
    for str in msg:
        params['message'] += f"{str}\n"

    res = my_bot.method("messages.send", params)

    print(res.json())