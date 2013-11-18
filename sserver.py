#!/usr/bin/env python

from socket import *
import time

s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost",5555))
s.listen(5)
client,addr = s.accept()
input = ''
print "Connection from %s:%d"%(addr[0],addr[1])
while 1:
    client, address = s.accept()
    data = client.recv(1024)
    while data:
        input += data
        client.send(data)
        data = client.recv(1024)
    client.close()
    break
print "Got data:\n", input

