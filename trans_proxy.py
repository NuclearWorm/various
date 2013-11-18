#!/usr/bin/env python

from socket import *
import sys, time, logging, random

LOG_FILENAME = '/tmp/proxy.log'
logging.basicConfig(filename=LOG_FILENAME, filemode = 'w', level=logging.DEBUG,)

def choppy_traffic(sck, data_tosend):

  timeout = 7 
  randoms = []
  rest = timeout
  for x in range(0, len(data_tosend)):
    tmp = random.random()
    randoms.append(tmp*rest)
    rest = rest - tmp*rest  

  if data_tosend:
    time_out = float(timeout)/len(data_tosend)
  else:
    print "Make sure you have data to send!"
    sys.exit(1)
  logging.debug("Time_out between requests is " + str(time_out) + " and req.length is " + str(len(data_tosend)) + \
                ", so the all timeout will be " + str(time_out*len(data_tosend)))
  start = time.time()
  for i in range(0, len(data_tosend)):
    try:
      sck.send(data_tosend[i])
    except Exception, e:
      print "sending ERROR!\n" + str(e)
      sys.exit(1)
    logging.debug("Sent '" + data_tosend[i] + "' and sleeping " + str(time_out) + " sec")
    time.sleep(randoms[i])
    
    
    #time.sleep(time_out)
  sck.send("\n\n")
  end = time.time()
  output = ''
  """
  get = sck.recv(1024)
  while get:
    output += get
    get = self.s.recv(1024)
  logging.debug("Output is " + output)
  print "Got output:\n", output
  logging.debug("Executed " + str(end -start) + " secs")
  self.s.close()
  """
  
  pass

### Start of cycle
while True:
  host = "192.168.2.138"
  port = 8123
  output = ''
  input = ''
  
  local_sock = socket(AF_INET, SOCK_STREAM)
  local_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  local_sock.bind(("", 5555))
  local_sock.listen(5)
  
  client,addr = local_sock.accept()
  logging.debug("Connection from %s:%d is established"%(addr[0], addr[1]))
  
  remote_sck = socket(AF_INET, SOCK_STREAM)
  remote_sck.connect((host, port))
  logging.debug("Connection TO %s:%d is established"%(host, port))
  
  data = client.recv(1024)
  logging.debug("Data received from %s is : %s"%(addr[0],data))
  
  
  
  
  while data:  
    try:
      
      ####  instead of remote_sck.send(data + "\n\n") - use garbaging traffic function
      choppy_traffic(remote_sck, data)
      logging.debug("Data sent to %s is : %s"%(host ,data))
    except Exception, e:
      logging.debug("Data send FAILED to %s : %s\nBecause %s"%(host ,data, str(e)))
      pass
    reply = remote_sck.recv(1024)
    while reply:
      logging.debug("Data received from %s is : %s"%(host ,reply))
      client.send(reply)
      logging.debug("Data sent to %s is : %s"%(addr[0] ,reply))
      output += reply
      reply = remote_sck.recv(1024)
    input += data
    
    #####  temporary - close socket
    client.close()
    remote_sck.close()
    local_sock.close()
    break
    #####  temporar - close socket
    
    data = client.recv(1024)
    if "endit" in data:
      break
  
### End of cycle
  
print "Output is ", output, " and input is ", input
"""client.close()
remote_sck.close()
local_sock.close()
"""


