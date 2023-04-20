import requests
from stem import Signal
from stem.control import Controller
from Printf import printf
from Randomize import randomize
from Validator import validator
from useragent import Useragent
from vars import proxies, protocols


class Proxy:
    def add(self, input: list):
        protocol = input[0].split(":")[0]
        ip = input[0].split(":")[1]
        port = input[0].split(":")[2]
        password = input[1]
        proxy_creds = {"protocol": protocol, "ip": ip, "port": port, "password": password}
        if not proxy_creds in list(proxies.values()):
            if validator.protocol(protocol):
                if validator.ip(ip):
                    if validator.port(port):
                        id = randomize.id()
                        proxies[id] = proxy_creds
                        # printf("Success: Proxy added with id '%s'" % id, mt="success")
                    else:
                        printf("Error: '%s' is not a valid port (valid: 0-65535)." % port, mt="error")
                else:
                    printf("Error: '%s' is not a valid ip address." % ip, mt="error")
            else:
                printf("Error: '%s' is not a valid protocol, valid protocols: %s" % (protocol, ",".join(protocols)), mt="error")
                printf("Info: Valid pattern (<protocol>:<ip>:<port>).", mt="info")
        else:
            printf("Warning: '%s:%s' is already added." % (ip, port), mt="warn")

    def is_online(self, proxy_data:dict):
        protocol: str = proxy_data['protocol']
        ip: str = proxy_data['ip']
        port: int = proxy_data['port']
        proxy = {'http': '%s://%s:%s' % (protocol, ip, port), 'https': '%s://%s:%s' % (protocol, ip, port)}
        msg = "Congratulations. This browser is configured to use Tor."

        try:
            return msg in requests.get("https://check.torproject.org", headers={"user-agent": Useragent.Devices().random()}, proxies=proxy).text
        except Exception:
            return False

    def get_identity(self, id:str, proxy_data:dict):
        protocol: str = proxy_data['protocol']
        ip: str = proxy_data['ip']
        port: int = proxy_data['port']
        proxy = {'http': '%s://%s:%s' % (protocol, ip, port), 'https': '%s://%s:%s' % (protocol, ip, port)}
        try:
            response = str(requests.get('https://api.ipify.org', headers={'user-agent': Useragent.Devices().random()}, proxies=proxy).text)
            printf(f"Info: {id} - [{ip}:{port}] - identity is '{response}'", mt="info")
        except Exception:
            printf(f"Error: attempt to get - [{ip}:{port}] - identity failed.", mt="error")

    def new(self, proxy_data:dict, controlPort:int):
        protocol: str = proxy_data['protocol']
        ip: str = proxy_data['ip']
        port: int = proxy_data['port']
        password: str = proxy_data['password']
        proxy = {'http': '%s://%s:%s' % (protocol, ip, port), 'https': '%s://%s:%s' % (protocol, ip, port)}
        try:
            response = str(requests.get("https://api.ipify.org", headers={"user-agent": Useragent.Devices().random()}, proxies=proxy).text)
            printf(f"Info: current - [{ip}:{port}] - identity is '{response}'", mt="info")

            with Controller.from_port(port=controlPort) as controller:
                controller.authenticate(password=password)
                controller.signal(Signal.NEWNYM)
                controller.close()
                response = str(requests.get("https://api.ipify.org", headers={"user-agent": Useragent.Devices().random()}, proxies=proxy).text)
            printf(f"Info: new - [{ip}:{port}] - identity is '{response}'", mt="info")
        except Exception:
            printf(f"Error: failed to get - [{ip}:{port}] - new identity.", mt="error")
proxy = Proxy()