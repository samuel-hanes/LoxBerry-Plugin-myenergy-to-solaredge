#!/usr/bin/python3

import socket

UDP_IP="127.0.0.1"
UDP_PORT=15555

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

try:
    # start the server listening on UDP socket
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.bind( (UDP_IP,UDP_PORT) )
    while True:
        data, addr = sock.recvfrom( 1024 ) # read data with buffer size of 1024 bytes
        data = str(data.decode('ascii'))
        print("<DEBUG> Received message:", data)

except:
    print("<ERROR> failed to bind socket!")
