#!/usr/bin/env python

from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost",5555))
output = ''
s.send("GET /\n")
get = s.recv(1024)
while get:
  output += get
  get = s.recv(1024)
print "Got output:\n", output
s.close()

