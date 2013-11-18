import time, sys
import asyncore, socket

from qikproto import parser, SignallingProtocol, MediaProtocol, presentation
import qiknet.scheduler
import logging

import qikrawparser

#import pprint

class MyProtocolHandler(asyncore.dispatcher):
  def __init__(self, address):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect(address)
    self.outFifo=str()
    self.sentcnt = 0

  def doSendData(self):
    if len(self.outFifo) > 0:
      res = self.send(self.outFifo)
      if isinstance(res, int):
        if res>0:
          self.outFifo = self.outFifo[res:]
          self.sentcnt = self.sentcnt + res
        else:
#          print 'Send res: %d'%res
          pass
        return res
      
  def writable(self):
    if not self.connected : return True
    if len(self.outFifo) > 0 : return True
#    if self.streaming : return True
    return False

  def readable(self):
    return True

  def handle_write(self):
    self.doSendData()

class QikClient(MyProtocolHandler):
  def __init__(self, address=('192.168.2.4', 11528)):
    MyProtocolHandler.__init__(self, address=address)
    self.parser = parser.Parser()
    if True:
      bufsz = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
      logging.debug('Sock buffer before: %d'%bufsz)
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
      bufsz = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
      logging.debug('Sock buffer after: %d'%bufsz)
    pass
  def sendPacket(self, pkt):
    self.outFifo = self.outFifo + pkt.getBytes()
    self.doSendData()
  def handle_read(self):
    data = self.recv(4096)
#    print 'Data received: %d'%len(data)
#    self.buffer = self.buffer + data
#    print 'buffered: %d'%len(self.buffer) 
    self.parser.push(data)
    res = self.parser.getPacket()
    while res:
      if res.protocol == presentation.PROTO_SIGNALLING:
        self.onSignallingPacket(res)
      elif res.protocol == presentation.PROTO_LOGGING:
        self.onLoggingPacket(res)
      elif res.protocol == presentation.PROTO_MEDIA:
        self.onMediaPacket(res)
      else:
        logging.warning("Unknown packet")
      res = self.parser.getPacket()
  
  
class QikTestUploadClient(QikClient):
  def __init__(self, scheduler, id=None, address=('192.168.2.4', 11528), bitrate=300, streamingDuration=0):
    self.id = id # just a representation name for logging
    self.connected = False
    self.streaming=False
    self.mediarefid=0
    self.bytessent=0
    self.scheduler = scheduler
    self.packetCnt = 0 # number of packets sent out
    self.lastts  = 0
    self.lastSize = 0
    self.streamingDuration = streamingDuration
    self.targetBitrate     = bitrate # kbps
    self.createTime = time.time()

    QikClient.__init__(self, address=address)
    
  def handle_connect(self):
    self.connected = True
    logging.info('%s : CONECTED in %g s'%(self.id, time.time() - self.createTime))
    self.sendPacket(SignallingProtocol.SessionStartPacket('c33b8d893097e29f16c1d75984c73ea7', refId=0))

  def handle_close(self):
    logging.info('%s : DISCONNECTED'%(self.id))
    self.close()
    self.connected = False
  
  def onSignallingPacket(self, pkt):
#    print 'Signalling handler'
    if pkt.opcode == SignallingProtocol.OPCODE_RES_OK :
#      logString('OPCODE_RES_OK, ref-id=%d'%pkt.ref_id)
      if pkt.ref_id == 0:
        #This is response to SESSION_START
        logging.info('%s : Session started in %g s'%(self.id, time.time() - self.createTime))
        self.sendPacket(SignallingProtocol.StreamStartPacket(refId=1))
      elif pkt.ref_id == 1:
        #This is response to STREAM_START
        logging.info('%s : Starting streaming in %g s'%(self.id, time.time() - self.createTime))
        self.streaming=True
        self.streamingStart = time.time()
        self.lastts  = time.time()
 #       self.scheduler.addTaskIn(self.onPeriodicTimer, (), 2)
        self.scheduler.addTaskIn(self.sendPacketConditionally, (), 0)
      elif  pkt.ref_id == 2:
        # This is response to STREAM_END
        self.scheduler.addTaskIn(self.endSessionTask, (), 0.001)
      elif  pkt.ref_id == 3:
        # This is response to SESSION_END
        logging.info('%s : Got response to session end'%(self.id))
    
  
  def sendPacketConditionally(self, scheduler, params):
    if (self.streamingDuration > 0) and ( time.time() > self.streamingStart + self.streamingDuration ):
      self.streaming = False
      self.scheduler.addTaskIn(self.stopStreamingTask, (), 0.001)
      return 
    DESIRED_INTERVAL = 0.1
    PKT_SIZE = int(self.targetBitrate*1000.0*DESIRED_INTERVAL/8) # bytes  
    self.doSendBigMediaPacket(self.packetCnt, PKT_SIZE)
    self.packetCnt = self.packetCnt + 1
    self.scheduler.addTaskIn(self.sendPacketConditionally, (), PKT_SIZE*8/self.targetBitrate/1000.0)
      
  def stopStreamingTask(self, scheduler, params):
    logging.info('%s : Sending STREAM_STOP'%(self.id))
    self.sendPacket(SignallingProtocol.StreamStopPacket(refId=2))
    
  def endSessionTask(self, scheduler, params):
    logging.info('%s : Sending SESSION_END'%(self.id))
    self.sendPacket(SignallingProtocol.SessionEndPacket(refId=3))

#  def onPeriodicTimer(self, scheduler, params):
#    currentts = time.time() 
#    sendingBitrate = (self.sentcnt-self.lastSize)/(currentts - self.lastts)*8/1000.0
#    self.lastts = currentts 
#    self.lastSize = self.sentcnt
#    self.lastSendingBitrate = sendingBitrate 
#    logString('%s : SENDING BITRATE: %g kbps'%(self.id, sendingBitrate))
#    if self.connected:      
#      self.scheduler.addTaskIn(self.onPeriodicTimer, (), 2)
  def doSendBigMediaPacket(self, ref, size):
    res = self.sendPacket(MediaProtocol.RandomVideoPacket(timestamp=ref, refId=ref, dataSize=size))
    pass
  def onLoggingPacket(self, pkt):
    pass
  def onMediaPacket(self, pkt):
    pass
  def getTotalDataSent(self):
    return self.bytessent


class HttpQRawDownloader(MyProtocolHandler):
  def __init__(self, address, streamId):
    MyProtocolHandler.__init__(self, address)
    self.connected = False
    self.qrawparser = qikrawparser.Parser()
    self.bytesreceived = 0
    self.streamId = streamId
    self.arrivalTime = {}  # Time of packet arrival, map ref-id -> time
    self.isHttpHeaderParsed = False
    self.lastChars = str()
  def handle_connect(self):
    self.connected = True
    logging.info('HTTP connected, Sending HTTP GET')
    self.outFifo = self.outFifo + 'GET /getFile?file=media.raw/%s.1 HTTP/1.0\r\n\r\n'%self.streamId
    self.doSendData()
  def handle_read(self):
    data = self.recv(4096)
    logging.debug('HTTP data:%d'%len(data))
    self.bytesreceived = self.bytesreceived + len(data)
    if not self.isHttpHeaderParsed:
      self.lastChars = self.lastChars + data
      idx1 = self.lastChars.find('\n\r\n')
      idx2 = self.lastChars.find('\n\n')
      if idx1 > 0:
        data = data[idx1+3:]
        self.isHttpHeaderParsed = True
      elif idx2 > 0:
        data = data[idx2+2:]
        self.isHttpHeaderParsed = True
      else:
        return
    
    self.qrawparser.push(data)
    res = self.qrawparser.getPacket()
#    if not res:
#      logging.info('File parser returned None')
    while res:
#      logging.info('Remaining data in buf: %d %d'%(len(self.qrawparser.buffer), self.qrawparser.filePacketHeaderLength))
#      pprint.pprint(res)
      
      if isinstance(res, qikrawparser.QikRawHeader) :
#        logging.info('Got file header')
        pass
      elif isinstance(res, qikrawparser.QikRawPacket) :
#        logging.info('Got file packet')
        self.onMediaPacket(res)
      else:
        logging.warning("Unknown packet")
      res = self.qrawparser.getPacket()
  def onMediaPacket(self, pkt):
    logging.debug('Media pkt %d'%pkt.ref_id)
    now = time.time()
    self.arrivalTime[pkt.ref_id] = now
    self.lastReceivedPktRefId = pkt.ref_id 

class QikTestLatencyClient(QikClient):
  def __init__(self, scheduler, id=None, address=('192.168.2.4', 11528), bitrate=300, streamingDuration=0):
    self.id = id # just a representation name for logging
    self.connected = False
    self.streaming=False
    self.mediarefid=0
    self.bytessent=0
    self.scheduler = scheduler
    self.packetCnt = 0 # number of packets sent out
    self.lastts  = 0
    self.lastSize = 0
    self.streamingDuration = streamingDuration
    self.targetBitrate     = bitrate # kbps
    self.createTime = time.time()
    
    self.httpclient = None
    self.httppin = (address[0], 9000)

    self.pktDepartureTime = {}  # Time of packet departure, map ref-id -> time

    QikClient.__init__(self, address=address)
    
  def handle_connect(self):
    self.connected = True
    logging.info('%s : CONECTED in %g s'%(self.id, time.time() - self.createTime))
    self.sendPacket(SignallingProtocol.SessionStartPacket('c33b8d893097e29f16c1d75984c73ea7', refId=0))

  def handle_close(self):
    logging.info('%s : DISCONNECTED'%(self.id))
    self.close()
    self.connected = False
  
  def onSignallingPacket(self, pkt):
#    print 'Signalling handler'
    if pkt.opcode == SignallingProtocol.OPCODE_RES_OK :
#      logString('OPCODE_RES_OK, ref-id=%d'%pkt.ref_id)
      if pkt.ref_id == 0:
        #This is response to SESSION_START
        logging.info('%s : Session started in %g s'%(self.id, time.time() - self.createTime))
        self.sendPacket(SignallingProtocol.StreamStartPacket(refId=1))
      elif pkt.ref_id == 1:
        #This is response to STREAM_START
        logging.info('%s : Starting streaming in %g s'%(self.id, time.time() - self.createTime))
        self.streaming=True
        for el in pkt.elements:
          if el.type=='BYTE16' and el.name==SignallingProtocol.ELEMENT_STREAM_UUID:
            #pprint.pprint(el.value)
            streamId = '%016x%016x'%el.value
            logging.info('%s : Got StreamId:%s'%(self.id, streamId))
        if not streamId:
          logging.warning('%s : No streamId in response'%self.id)
        self.httpclient = HttpQRawDownloader(self.httppin, streamId)
        
        self.streamingStart = time.time()
        self.lastts  = time.time()
 #       self.scheduler.addTaskIn(self.onPeriodicTimer, (), 2)
        self.scheduler.addTaskIn(self.sendPacketConditionally, (), 0)
      elif  pkt.ref_id == 2:
        # This is response to STREAM_END
        self.scheduler.addTaskIn(self.endSessionTask, (), 0.001)
      elif  pkt.ref_id == 3:
        # This is response to SESSION_END
        logging.info('%s : Got response to session end'%(self.id))
    
  
  def sendPacketConditionally(self, scheduler, params):
    if (self.streamingDuration > 0) and ( time.time() > self.streamingStart + self.streamingDuration ):
      self.streaming = False
      self.scheduler.addTaskIn(self.stopStreamingTask, (), 0.001)
      return 
    DESIRED_INTERVAL = 0.1
    PKT_SIZE = int(self.targetBitrate*1000.0*DESIRED_INTERVAL/8) # bytes  
    self.doSendBigMediaPacket(self.packetCnt, PKT_SIZE)
    self.pktDepartureTime[self.packetCnt] = time.time() 
    self.packetCnt = self.packetCnt + 1
    self.scheduler.addTaskIn(self.sendPacketConditionally, (), PKT_SIZE*8/self.targetBitrate/1000.0)
      
  def stopStreamingTask(self, scheduler, params):
    logging.info('%s : Sending STREAM_STOP'%(self.id))
    self.sendPacket(SignallingProtocol.StreamStopPacket(refId=2))
    
  def endSessionTask(self, scheduler, params):
    logging.info('%s : Sending SESSION_END'%(self.id))
    self.sendPacket(SignallingProtocol.SessionEndPacket(refId=3))

#  def onPeriodicTimer(self, scheduler, params):
#    currentts = time.time() 
#    sendingBitrate = (self.sentcnt-self.lastSize)/(currentts - self.lastts)*8/1000.0
#    self.lastts = currentts 
#    self.lastSize = self.sentcnt
#    self.lastSendingBitrate = sendingBitrate 
#    logString('%s : SENDING BITRATE: %g kbps'%(self.id, sendingBitrate))
#    if self.connected:      
#      self.scheduler.addTaskIn(self.onPeriodicTimer, (), 2)
  def doSendBigMediaPacket(self, ref, size):
    res = self.sendPacket(MediaProtocol.RandomVideoPacket(timestamp=ref, refId=ref, dataSize=size))
    pass
  def onLoggingPacket(self, pkt):
    pass
  def onMediaPacket(self, pkt):
    pass
  def getTotalDataSent(self):
    return self.bytessent

