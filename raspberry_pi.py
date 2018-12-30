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

def myfunc(device, lock, fn):
    for n in range(1000):
        lock.acquire()        
        connection = http.client.HTTPConnection(url)
        connection.request(method="POST", url="/", body=fn(device, n))
        connection.close()
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

# POST info to server
connection = http.client.HTTPConnection(url)
connection.request(method="POST", url="/info", body="devices:3")
connection.close()

print("Starting GPIO simulator")
# start simulated devices (one thread per device)
thread1 = Thread(target=myfunc, args=("1", theLock, f1))
thread2 = Thread(target=myfunc, args=("2", theLock, f2))
thread3 = Thread(target=myfunc, args=("3", theLock, f3))

thread1.start()
thread2.start()
thread3.start()
 
thread1.join()
thread2.join()
thread3.join()
 
print("\nRaspberry Pi terminating") 
 


