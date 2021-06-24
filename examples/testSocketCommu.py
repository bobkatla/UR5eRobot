import socket
import time

HOST = "192.168.122.1"
PORT = 30000

print ('starting program')

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s = socket.socket()
s.bind((HOST, PORT))
s.listen()
print("Here")
(c, addr) = s.accept()
msg = c.recv(1024)
print(msg)


s.close()