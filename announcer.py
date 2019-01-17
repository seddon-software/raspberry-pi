from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from constants import MAGIC, PORT

def get_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
#my_ip= gethostbyname(gethostname()) #get our IP. Be careful if you have multiple network interfaces or IPs
my_ip = get_ip()
print(f"announcer: {my_ip}")

def broadcastServerAddress():
    while 1:
        data = f"{MAGIC}:{my_ip}:{PORT}"
        s.sendto(data.encode(), ('<broadcast>', PORT))
        sleep(5)

from threading import Thread
Thread(target=broadcastServerAddress).start()



    