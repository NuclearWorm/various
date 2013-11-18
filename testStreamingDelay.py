#!/usr/bin/env python

# command line: desired bitrate for each channel, max packet size, number of channels, start delay (between channels), test duration, packet_size

import time, sys
from optparse import OptionParser
import qiknet.scheduler
import TestClient

import logging

VERSION='0.1.a.3'

class StreamTestBench(object):
  def __init__(self):
    self.clients = []
    self.lastTs = time.time()
    self.lastByteCnt = {}
    self.lastRcvByteCnt = {}
    self.lastAnalyzedRefid = {}
    self.useCompactPrinting = True
    
  def createClient(self, scheduler, (name, bitrate, duration, host)):
    ch = TestClient.QikTestLatencyClient(scheduler = scheduler, id=name, address=(host, 11528), bitrate=bitrate, streamingDuration=duration)
    self.clients.append(ch)

  def onPeriodicTimer(self, scheduler, params):
    currentts = time.time()
    onLine = False # atleast one client connected
    
    #Calculate Sending bitrate
    sendingBitrate = {}
     
    for client in self.clients:
      id = client.id
      if id not in self.lastByteCnt:
        self.lastByteCnt[id] = 0
      sendingBitrate[id] = (client.sentcnt - self.lastByteCnt[id])/(currentts - self.lastTs)*8/1000.0
      self.lastByteCnt[id] = client.sentcnt
      if not self.useCompactPrinting: 
        logging.info('%s : SENDING BITRATE: %.1f kbps'%(id, sendingBitrate[id]))
      if client.connected:
        onLine = True
    
    totalBr = reduce(lambda a,b:a+b, sendingBitrate.values(), 0)
    if self.useCompactPrinting:
      bitrateStr = reduce(lambda s1,s2:'%s %s'%(s1,s2), [ '%s:%.1f'%(i,sendingBitrate[i]) for i in sorted(sendingBitrate.keys())])
      logging.info('SENDING BITRATE: %s Total=%.1f kbps'%(bitrateStr, totalBr))
    else:
      logging.info('TOTAL SENDING BITRATE: %.1f kbps'%(totalBr))
       
    #Calculate Receiving bitrate
    receivingBitrate = {}
     
    for client in self.clients:
      id = client.id
      if id not in self.lastRcvByteCnt:
        self.lastRcvByteCnt[id] = 0
        
      if client.httpclient:
        logging.debug('HTTP FIFO :%d', len(client.httpclient.qrawparser.buffer))
        receivingBitrate[id] = (client.httpclient.bytesreceived - self.lastRcvByteCnt[id])/(currentts - self.lastTs)*8/1000.0
        self.lastRcvByteCnt[id] = client.httpclient.bytesreceived
        if not self.useCompactPrinting: 
          logging.info('%s : RECEIVING BITRATE: %.1f kbps'%(id, receivingBitrate[id]))
        if client.connected:
          onLine = True

    totalBr = reduce(lambda a,b:a+b, receivingBitrate.values(), 0)
    if self.useCompactPrinting:
      bitrateStr = reduce(lambda s1,s2:'%s %s'%(s1,s2), [ '%s:%.1f'%(i,receivingBitrate[i]) for i in sorted(receivingBitrate.keys())], '')
      logging.info('RECEIVING BITRATE: %s Total=%.1f kbps'%(bitrateStr, totalBr))
    else:
      logging.info('TOTAL RECEIVING BITRATE: %.1f kbps'%(totalBr))
    
    
    #Calculate delay
    latency = {}

    for client in self.clients:
      id = client.id
        
      if client.httpclient and hasattr(client.httpclient, 'lastReceivedPktRefId'):
        if id not in self.lastAnalyzedRefid:
          self.lastAnalyzedRefid[id] = -1
        
        logging.debug('last ref-id:%d'%self.lastAnalyzedRefid[id])
        
        max_delay = 0;
        for refid in range(self.lastAnalyzedRefid[id]+1, client.httpclient.lastReceivedPktRefId):
          logging.debug('Arrival time for ref-id %d is %f'%(refid, client.httpclient.arrivalTime[refid]))          
          logging.debug('Departure time for ref-id %d is %f'%(refid, client.pktDepartureTime[refid]))          
          delay = client.httpclient.arrivalTime[refid] - client.pktDepartureTime[refid]
          logging.debug('Delay for ref-id %d is %f'%(refid, delay))          
          if delay > max_delay:
            max_delay = delay
        
        latency[id] = max_delay
        
        self.lastAnalyzedRefid[id] = client.httpclient.lastReceivedPktRefId
        
        if not self.useCompactPrinting: 
          logging.info('%s : LATENCY: %.1f ms'%(id, latency[id]*1000))

    maxLatency = max(latency.values())
    if self.useCompactPrinting:
      latencyStr = reduce(lambda s1,s2:'%s %s'%(s1,s2), [ '%s:%.1f'%(i,latency[i]*1000) for i in sorted(latency.keys())], '')
      logging.info('LATENCY: %s MAX=%.1f ms'%(latencyStr, maxLatency*1000))
    else:
      logging.info('MAX LATENCY: %.1f ms'%(maxLatency*1000))
    
    
    self.lastTs = currentts
    
       
       
  #    self.lastSendingBitrate = sendingBitrate 
    if onLine:      
      scheduler.addTaskIn(self.onPeriodicTimer, (), 2)

  def run(self):
    parser = OptionParser(version='%prog['+VERSION+']')
    parser.add_option("-n", action="store", type="int", default=1, dest="clients", help="How many clients to run")
    parser.add_option("-d", action="store", type="int", default=5, dest="delay", help="Delay between client start, default is 5 sec")
    parser.add_option("-t", action="store", type="int", default=0, dest="duration", help="Test duration, default is 0 - unlimited")
    parser.add_option("-r", "--bitrate", action="store", type="int", default=300, dest="bitrate", help="Streaming bitrate, kbps")
    parser.add_option("-H", '--host', action="store", type="string", default='edge1.stage.qik.com', dest="host", help="Edge server address")
    parser.add_option("-l", action="store_true", dest="use_long", help="Print bitrate for each channel on separate line")
    (options, args) = parser.parse_args()
    
    if options.use_long:
      self.useCompactPrinting = False
      
    self.sch = qiknet.scheduler.MyScheduler()
  
    timestrart=time.time()
    for i in range(0, options.clients):
      self.sch.addTaskAt(self.createClient, ('c%d'%i, options.bitrate, options.duration, options.host), timestrart + i*options.delay)

    self.sch.addTaskIn(self.onPeriodicTimer, (), 2)
  
    self.sch.run(use_poll=True)

if __name__ =="__main__":
#  logging.basicConfig(format="%(asctime)s.%(msecs).03d [Module=%(module)s] [L=%(levelname)s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
  logging.basicConfig(format="%(asctime)s.%(msecs).03d %(message)s", datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
  testbench = StreamTestBench()
  testbench.run()
