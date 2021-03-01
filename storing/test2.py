#!/usr/bin/env python

# Echo client program
import socket
import time
HOST = "10.42.0.1" # The remote host
PORT = 30000 # The same port as used by the server
print "Starting Program"
count = 0
 
while (count < 1000):
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 s.bind((HOST, PORT)) # Bind to the port 
 s.listen(5) # Now wait for client connection.
 c, addr = s.accept() # Establish connection with client.
 try:
   msg = c.recv(1024)
   print "Pose Position = ", msg
   msg = c.recv(1024)
   print "Joint Positions = ", msg
   msg = c.recv(1024)
   print "Request = ", msg
   time.sleep(1)
   if msg == "asking_for_data":
     count = count + 1
   print "The count is:", count
   time.sleep(0.5)
   print ""
   time.sleep(0.5)
   c.send("(200,50,45)");
   print "Send 200, 50, 45"
 except socket.error as socketerror:
   print count
 
c.close()
s.close()
print "Program finish"
