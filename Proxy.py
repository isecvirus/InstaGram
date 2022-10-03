import requests
from stem import Signal
from stem.control import Controller
from Printf import printf
from useragent import Useragent


class Proxy:
    def is_online(self, proxy_data:dict):
        protocol: str = proxy_data['protocol']
        ip: str = proxy_data['ip']
        port: int = proxy_data['port']
        proxy = {'http': '%s://%s:%s' % (protocol, ip, port), 'https': '%s://%s:%s' % (protocol, ip, port)}
        msg = "Congratulations. This browser is configured to use Tor."

        try:
            return (msg in requests.get("https://check.torproject.org", headers={"user-agent": Useragent.Devices().random()}, proxies=proxy).text)
        except Exception:
            return False
    def get_identity(self, id:str, proxy_data:dict):
        protocol: str = proxy_data['protocol']
        ip: str = proxy_data['ip']
        port: int = proxy_data['port']
        proxy = {'http': '%s://%s:%s' % (protocol, ip, port), 'https': '%s://%s:%s' % (protocol, ip, port)}
        try:
            response = str(requests.get('https://api.ipify.org', headers={'user-agent': Useragent.Devices().random()}, proxies=proxy).text)
            printf(f"Info: {id} identity is '{response}'", mt="info")
        except Exception:
            printf(f"Error: attempt to get identity failed.", mt="error")

    def new(self, id:str, proxy_data:dict, controlPort:int):
        protocol: str = proxy_data['protocol']
        ip: str = proxy_data['ip']
        port: int = proxy_data['port']
        password: str = proxy_data['password']
        proxy = {'http': '%s://%s:%s' % (protocol, ip, port), 'https': '%s://%s:%s' % (protocol, ip, port)}
        try:
            response = str(requests.get("https://api.ipify.org", headers={"user-agent": Useragent.Devices().random()}, proxies=proxy).text)
            printf(f"Info: current identity is '{response}'", mt="info")

            with Controller.from_port(port=controlPort) as controller:
                controller.authenticate(password=password)
                controller.signal(Signal.NEWNYM)
                controller.close()
                response = str(requests.get("https://api.ipify.org", headers={"user-agent": Useragent.Devices().random()}, proxies=proxy).text)
            printf(f"Info: new identity is '{response}'", mt="info")
        except Exception:
            printf(f"Error: failed to get new identity for {id}.", mt="error")
proxy = Proxy()