import random
import time
import sys
import http.client

for n in range(100):
    connection = http.client.HTTPConnection("192.168.0.89:5559")
    data = connection.request(method="GET", url="/")
    print(data[:-5])

