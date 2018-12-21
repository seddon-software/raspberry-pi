from socket import socket, AF_INET, SOCK_DGRAM
from constants import MAGIC, PORT

s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
s.bind(('', PORT))

while 1:
    data, addr = s.recvfrom(1024) #wait for a packet
    data = data.decode()
    if data.startswith(MAGIC):
        print("got service announcement from", data[len(MAGIC):])
