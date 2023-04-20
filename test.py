# Examination Lab! (:
import itertools
import random
import threading
import time


passwords = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"] # 13
proxies =   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # 10
good = {"h": True}
stop_threads = False
threads = []
added = []

def job(proxy, password):
    global stop_threads
    if password in good:
        print("FOUND:", proxy, password)
        stop_threads = True
    if stop_threads:
        return
    added.append(f"{proxy}:{password}")
    time.sleep(random.randint(1, 10))

for password, proxy in zip(passwords, itertools.cycle(proxies)):
    thread = threading.Thread(target=job, args=(proxy, password,))
    thread.start()
    threads.append(thread)

for trd in threads:
    trd.join()

print(added)