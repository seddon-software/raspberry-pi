from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from threading import Thread
from constants import MAGIC, PORT

s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
s.bind(('', PORT))

url = None

def getServerUrl():
    return url

def receiveServerAnnouncement():
    global url
    while True:
        data, _ = s.recvfrom(1024) #wait for a packet
        data = data.decode()
        if data.startswith(MAGIC):
            _, SERVER_IP, SERVER_PORT = data.split(":")
            url = f"{SERVER_IP}:{SERVER_PORT}"
            s.close()
            break

def startDiscoverer():
    Thread(target=receiveServerAnnouncement).start()
