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

To Install Python on Raspberry Pi
=================================
	
1. Download Python-3.6.1.tar.xz from https://www.python.org/

2. Unzip the file and then use the commands:
	./configure
	make
	make test
	sudo make install
This will install Python 3.6 but pip3 may not be working.

3. Install necessary modules using:
	sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

4. Configure pip:
	sudo make
	sudo make install

5. Now you should be able to use pip, e.g.:
	sudo pip3 install numpy

To Setup Software on Raspberry Pi
=================================
1. Choose a directory on the pi, and cd to it:
	/home/pi

2. Perform a git clone:
	git clone https://github.com/seddon-software/raspberry-pi.git


To run server.py and raspberry_pi.py at boot on the pi
======================================================

1. Edit /etc/rc.local and add the following lines:
	sudo /usr/local/bin/python /home/pi/p/server.py &
	sudo /usr/local/bin/python /home/pi/p/raspberry_pi.py &
	
where /usr/local/bin/python is the python being used and /home/pi/p is the directory with our software installed

2. If there are errors on boot, you can see the boot log with:
	systemctl status rc.local.service
	