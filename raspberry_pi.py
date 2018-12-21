############################################################
#
#    creating threads
#
############################################################

import random
import time
import sys
import http.client


# import http.client
# 
# connection = http.client.HTTPConnection("192.168.0.89:5559")
# connection.request("GET", "/")
# response = connection.getresponse()
# print("Status: {} and reason: {}".format(response.status, response.reason))
# 
# connection.close()


h1 = http.client.HTTPConnection("192.168.0.89:5559")
print("client")
h1.request(method="POST", url="http://192.168.0.89:5559", body="hello from Chris")
h1 = http.client.HTTPConnection("192.168.0.89:5559")
h1.request(method="POST", url="/", body="hello from Seddon")

from threading import Thread, Lock
theLock = Lock()

def f1(id, n):
    return f"{id}:{n%10}"

def f2(id, n):
    return f"{id}:{n%5}"

def f3(id, n):
    return f"{id}:{n%3}"

def myfunc(id, lock, fn):
    for n in range(1000):
        lock.acquire()        
        connection = http.client.HTTPConnection("192.168.0.89:5559")
        connection.request(method="POST", url="/", body=fn(id, n))
        connection.close()
        lock.release()    
        time.sleep(random.random() * 0.1)

 
# define a callback function - to be called via start()
thread1 = Thread(target=myfunc, args=("1", theLock, f1))
thread2 = Thread(target=myfunc, args=("2", theLock, f2))
thread3 = Thread(target=myfunc, args=("3", theLock, f3))
 
thread1.start()
thread2.start()
thread3.start()
 
thread1.join()
thread2.join()
thread3.join()
 
print("\nEnd of main Thread") 
 


