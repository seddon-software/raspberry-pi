import http.client

h1 = http.client.HTTPConnection("192.168.0.89:5559")
print("client")
h1.request(method="POST", url="http://192.168.0.89:5559", body="hello from Chris")

