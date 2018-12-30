This program suite is in 3 parts.

1. Raspberry Pi software:
	raspberry_pi.py
	discoverer.py

2. Server software:
	server.py
	announcer.py
	constants.py
	
3. Client (browser) software:
	graph.html
	client/*
	
Operation
=========
1. The server should be started first.
		The server will broadcast its IP and PORT on the local 
		network and await data from the raspberry pi.
2. The raspberry pi can now be started.
		The raspberry pi will locate the server and then start sending data to the server
		At present the software uses a simulator for the GPIO data
3. Fire up a browser on a device connected to the local network and then connect to the server.  
	The browser cannot use server discovery because of restrictions in the http protocol, so 
	you must connect manually.  For example use the URL:
		http://localhost:5559/graph.html
	At present I am assuming the raspberry pi is sending data in the range 0 to 10.  It is fairly 
	simple to allow different ranges.