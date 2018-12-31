############################################################
#
#    Raspberry Pi program
#
############################################################

# The Raspberry Pi needs to detect the server before it can send data; this
# is done by the discoverer code (imported below)
# 
# The program then sends data to the server using a POST http message.
# The messages are sent from all monitored devices; the form of an individual message is simply:
#    <deviceNo>:<int value>
# Each device sends its messages separately

import random
import time
import http.client
import json
from threading import Thread, Lock
from discoverer import getServerUrl, startDiscoverer

theLock = Lock()

def f1(device, n):
    n = n % 10
    n += random.random()
    return f"{device}:{n}"

def f2(device, n):
    return f"{device}:{n%5}"

def f3(device, n):
    return f"{device}:{n%3}"

def f4(device, n):
    return f"{device}:{n%7}"

def f5(device, n):
    return f"{device}:{n%21}"

def myfunc(device, lock, fn):
    for n in range(1000):
        lock.acquire()
        requests.post(f"http://{url}", data=fn(device, n))
        lock.release()    
        time.sleep(random.random() * 0.1)
        time.sleep(1)

print("Raspberry Pi Client\n")
 
startDiscoverer()
print("... attempting to locate server")

# wait for server to be discovered
while True:
    url = getServerUrl()
    if url: break
    time.sleep(5)
print(f"... server located: {url}")

# POST init data to server
import requests

#connection = http.client.HTTPConnection(url)
headers = {'Content-type': 'application/json'}
body = [{"device1":{"name":"pressure", "min":0.0, "max":10.0}}, 
        {"device2":{"name":"temperature", "min":0.0, "max": 5.0}}, 
        {"device3":{"name":"height", "min":0.0, "max": 3.0}}, 
        {"device4":{"name":"width", "min":0.0, "max": 8.0}}, 
        {"device5":{"name":"length", "min":0.0, "max":24.0}}]

r = requests.post(f"http://{url}/init", json=body)


# start simulated devices (one thread per device)
print("Starting GPIO simulator")

threads = []
for n in range(1, 6):
    thread = Thread(target=myfunc, args=(f"{n}", theLock, globals()[f"f{n}"]))
    threads.append(thread)
    thread.start()

for n in range(1, 6):
    threads[n-1].join()
# thread2 = Thread(target=myfunc, args=("2", theLock, f2))
# thread3 = Thread(target=myfunc, args=("3", theLock, f3))
# thread4 = Thread(target=myfunc, args=("4", theLock, f4))
# thread5 = Thread(target=myfunc, args=("5", theLock, f5))
# 
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
 
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
 
print("\nRaspberry Pi terminating") 
 


