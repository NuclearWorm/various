#!/usr/bin/env python

from test_client import EdgeClient
import tpro.qraw.qraw as qraw

import sys, time
#qraw    = qik.qraw.qraw

class LiveTest:
  def __init__(self, home_dir, host, file, device_id = '0eaadaacd47901fabefee1d7fbd4062b'):
    self.home_dir = home_dir
    self.host = host
    self.device_id = device_id
    self.file = file
    pass
  
  def run(self):
    reader = qraw.FileReader(self.file)
    main_header = reader.GetMainHeader()
    mpackets = 0
    sizesum = 0
    times = []
    client = EdgeClient(self.host,device_id = "b"*32 )
    
    times.append(time.time())
    session_uuid = client.startSession()
    if None != session_uuid:
      stream_uuid = client.startStream(qraw_header = main_header)
      print "====================================================";
      print "Session ID: %s\nStream ID: %s"%(session_uuid, stream_uuid)
    times.append(time.time())
    packet = reader.ReadNextPacket()
    
    while None != packet:
      client.sendMediaPacket(packet)
      mpackets=mpackets+1
      sizesum=sizesum+len(packet.payload)
      packet = reader.ReadNextPacket()
    times.append(time.time())  
    client.stopStream()
    client.stopSession()
    times.append(time.time())
    print "Sent %d packets, summary %d bytes, took %d secs, avg rate - %d Kbps"%(mpackets, sizesum, times[3] - times[0], (sizesum*8/1024)/(times[2] - times[1]))
    print "====================================================";
    client.done()
    pass
  
  def report(self):
    
    pass
  

def main(*args):
  test = LiveTest('/home/serg/testscripts/various1/testscripts', '192.168.2.4', '/home/serg/tmp/Videos/streams/006_mpeg4_640x480_amrnb_021268ed86964454b2b55571065369bc.1')
  test.run()
  
  
  pass

if __name__ =='__main__':
  main(sys.argv)
 