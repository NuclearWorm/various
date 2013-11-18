#!/usr/bin/env python

import select
import socket
import sys
import threading
import time, logging, random
from optparse import OptionParser

VERSION='0.2.a.1'
LOG_FILENAME = '/tmp/proxy.log'
logging.basicConfig(filename=LOG_FILENAME, filemode = 'w', level=logging.DEBUG,)

class Server:
  def __init__(self, local_port, remote_port, remote_host):
    self.host = ''
    self.rhost = remote_host
    self.port = local_port
    self.rport = remote_port
    
    self.backlog = 5
    self.size = 1024
    self.server = None
    self.threads = []

  def open_socket(self):
    try:
      self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.server.bind((self.host,self.port))
      self.server.listen(5)
    except socket.error, (value,message):
      if self.server:
        self.server.close()
      print "Could not open socket: " + message
      sys.exit(1)

  def run(self):
    
    
    self.open_socket()
    input = [self.server,sys.stdin]
    running = 1
    while running:
      inputready,outputready,exceptready = select.select(input,[],[])

      for s in inputready:

        if s == self.server:
          # handle the server socket
          try:
            c = Client(self.server.accept(), self.rhost, self.rport)
            c.start()
            self.threads.append(c)
            logging.debug("Successfully connect with new client thread! ")
          except Exception, e:
            print "Can't connect! Got ERROR: ", e
            logging.debug("Can't connect with new client thread! Got ERROR: " + str(e))
            pass
          
        elif s == sys.stdin:
          # handle standard input
          junk = sys.stdin.readline()
          running = 0

    # close all threads

    self.server.close()
    for c in self.threads:
      c.join()
    
class Client(threading.Thread):
  def __init__(self,(client,address), rhost, rport):
    threading.Thread.__init__(self)
    self.client = client
    self.address = address
    self.size = 1024
    self.rport = rport
    self.rhost = rhost
    try:
      self.remote_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.remote_sck.connect((self.rhost, self.rport))
      logging.debug("Running thread with " + str([self.client, self.address, self.size, \
         self.rport, self.rhost, self.remote_sck]))
    except Exception, e:
      #print "Got ERROR: ", e
      logging.debug("Got error from clients thread: "+ str(e))
      self.remote_sck.close()
      self.client.close()
      logging.debug("Got error from clients thread and closed sockets, raised 'connect error'\n" + "Can NOT connect to %s:%s !"%(rhost, rport) + str(e))
      raise NameError('Can NOT connect to %s:%s !'%(rhost, rport) + str(e))
      
  def run(self):
    
    def choppy_traffic(sck, data_tosend):
      
      strategy = 2
      timeout = 6
      delays = []
      rest = timeout
      logging.debug("Start sending choppy traffic: socket %s and len(data) = %d" % (sck, len(data)))
      if strategy == 1:
        for x in range(0, len(data_tosend)):
          tmp = random.random()
          delays.append(tmp*rest)
          rest = rest - tmp*rest
        random.shuffle(delays)
        logging.debug("Strategy 1: Array of random timeouts is " + str(delays))
      elif strategy == 2:
        time_out = float(timeout)/len(data_tosend)
        delays = [time_out]*len(data_tosend)
        logging.debug("Strategy 2: Array of regular timeouts is " + str(delays))
      elif strategy == 3:
        for x in range(0, len(data_tosend)):
          tmp = random.random()
          delays.append(tmp*timeout)
        logging.debug("Strategy 3: Array of random timeouts is " + str(delays))
      #elif strategy == 4:
        
        
        
        
      else:
        logging.debug("Make sure you choose strategy from 1 to 3!")
        sys.exit(1)
      #logging.debug("Time_out between requests is " + str(time_out) + " and req.length is " + str(len(data_tosend)) + \
      #      ", so the all timeout will be " + str(time_out*len(data_tosend)))
      start = time.time()
      for i in range(0, len(data_tosend)):
        try:
          sck.send(data_tosend[i])
          logging.debug("$$$$$$$  choppy_traffic sent: '%s'"%data_tosend[i])
        except Exception, e:
          logging.debug("sending ERROR!\n" + str(e))
          sys.exit(1)
        logging.debug("$$$$$$$  choppy_traffic sleep: " + str(delays[i]) + " sec")
        time.sleep(delays[i])
      end = time.time()
      logging.debug("All sending of data above took %.2f sec"%(end - start))
    ###                   ###
    ### Start of function ###
    ###                   ###  
    running = 1
    while running:
      data = self.client.recv(self.size)
      logging.debug("Data received from %s:%s is : %s"%(self.address[0],self.address[1] , data))
      if data:
        choppy_traffic(self.remote_sck, data)
        logging.debug(" **** CHOPPED **** Data sent to %s is : %s"%(self.rhost ,data))
        reply = self.remote_sck.recv(self.size)
        while reply:
          logging.debug("Data received from %s is : %s"%(self.rhost ,reply))
          self.client.send(reply)
          logging.debug("Data sent to %s:%s is : %s"%(self.address[0] ,self.address[1] ,reply))
          reply = self.remote_sck.recv(self.size)
        #self.remote_sck.close()
      else:
        self.client.close()
        ## Added from "if" state:
        self.remote_sck.close()
        running = 0

if __name__ == "__main__":
  parser = OptionParser(version='%prog['+VERSION+']')
  parser.add_option("-l", action="store", type="int", default=5555, dest="local_port", help="Local port for listening")
  parser.add_option("-p", action="store", type="int", default=80, dest="remote_port", help="Port of remote host connect to")
  parser.add_option("-r", action="store", type="string", default="yandex.ru", dest="remote_host", help="Remote host")
  parser.add_option("-d", action="store_true", default=False, dest="debug", help="Debug mode on")
  (options, args) = parser.parse_args()
  logging.debug("Parameters: " + str([options.local_port, options.remote_port, options.remote_host, options.debug]))
  s = Server(options.local_port, options.remote_port, options.remote_host)
  s.run() 