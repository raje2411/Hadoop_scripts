#!/usr/bin/env python
import socket
import subprocess
import sys
from datetime import datetime

# Ask for input
try:
    remoteServer = raw_input("Enter a remote hostname: ")
    ports = []
    ports = list(map(int,raw_input("Enter the ports to scan: ").strip().split(',')))[:]
    print ports
    remoteServerIP = socket.gethostbyname(remoteServer)
except ValueError:
    print "+" * 65
    print ports
    print "ERROR: Check the inputs values given for remote server and port "
    print "+" * 65
    sys.exit(3)
except socket.timeout:
    print "+" * 65
    print "ERROR: Timeout - Not able to connect to remote host.  Check if you are able to connect to remote machine"
    print "+" * 65
    sys.exit(2)
except socket.gaierror:
    print "+" * 65
    print "ERROR:  Not able to resolve the hostname.  Check the input hostname"
    print "+" * 65
    sys.exit(1)

if ports[0] == 1:
    print "\nNo input ports given, testing the predefined ports\n"
    ports = [10000,10001,10002]
t1 = datetime.now()

# Print a nice banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning remote host", remoteServer,"(",remoteServerIP,")"
print "\nStart time :", t1
print "-" * 60


# We also put in some error handling for catching errors
try:
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        print result
        if result == 0 :
            print "Port {}\t: 	 Open".format(port)
        else:
            print "Port {}\t: 	 Not able to connect".format(port)
        sock.close()
    print "-" * 60
except KeyboardInterrupt :
    print "You pressed Ctrl+C"
    sys.exit()
except socket.gaierror :
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
except socket.error :
    print "Couldn't connect to server"
    sys.exit()

# Checking the time again
t2 = datetime.now()
# Calculates the difference of time, to see how long it took to run the script
total = t2 - t1
# Printing the information to screen
print '\nScanning Completed in: ', total
print "-" * 60
