import struct

class QikRawHeader(object):
  pass

class QikRawPacket(object):
  pass

class Parser(object):
  def __init__(self):
    self.buffer = str()
    self.waitHdrState = True
    self.fileHeaderFormat = '>IIIIIIIII'
    self.fileHeaderLength = struct.calcsize(self.fileHeaderFormat)
    self.filePacketHeaderFormat = '>IBBII'
    self.filePacketHeaderLength = struct.calcsize(self.filePacketHeaderFormat)
  def push(self, data):
    self.buffer = self.buffer + data
#    print 'buffered: %d'%len(self.buffer)
  def getPacket(self):
    if self.waitHdrState:
      if len(self.buffer) >= self.fileHeaderLength:
         filehdr = struct.unpack(self.fileHeaderFormat, self.buffer[:self.fileHeaderLength])
         self.buffer = self.buffer[self.fileHeaderLength:]
         hdr = QikRawHeader()
         hdr.__dict__['version']         = filehdr[0]
         hdr.__dict__['VideoCodec']      = filehdr[1]
         hdr.__dict__['VideoHSize']      = filehdr[2]
         hdr.__dict__['VideoVSize']      = filehdr[3]
         hdr.__dict__['VideoClockNum']   = filehdr[4]
         hdr.__dict__['VideoClockDenum'] = filehdr[5]
         hdr.__dict__['AudioCodec']      = filehdr[6]
         hdr.__dict__['AudioClockNum']   = filehdr[7]
         hdr.__dict__['AudioClockDenum'] = filehdr[8]
#         print '$$$ file hdr, %d %d %d %d %d %d %d %d %d'%filehdr
         self.waitHdrState = False
         return hdr
    else:
      if len(self.buffer) >= self.filePacketHeaderLength:
        pkthdr = struct.unpack(self.filePacketHeaderFormat, self.buffer[:self.filePacketHeaderLength])
        (pkt_len, opcode, idx, ref_id, ts) = pkthdr
#        print '### got pkt hdr, len=%d'%pkt_len
        if len(self.buffer) >= pkt_len: 
          if  pkt_len > self.filePacketHeaderLength:
            payload = self.buffer[self.filePacketHeaderLength:pkt_len]
          else:
            payload = None
          self.buffer = self.buffer[pkt_len:]
          pkt = QikRawPacket()
          pkt.__dict__['opcode'] = opcode
          pkt.__dict__['idx'] = idx
          pkt.__dict__['ref_id'] = ref_id
          pkt.__dict__['timestamp'] = ts
          pkt.__dict__['payload'] = payload
          return pkt
