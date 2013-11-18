import struct
import random
randData = ''.join( k for k in [chr(c) for c in [random.randint(0,255) for i in range(0,100000)]])
#print 'Rand data size: %d'%len(randData)

from qikproto.presentation import encodeBlobElement
class RandomVideoPacket(object):
  def __init__(self, timestamp, refId, dataSize):
    self.timestamp = timestamp
    self.refId = refId
    self.dataSize = dataSize
  def getBytes(self):
    
    payload = encodeBlobElement(randData[0:self.dataSize], 0x0000)
                
    packetSize = 12 + len(payload)
#    print 'Packet size: %d'%packetSize
    result = struct.pack('!BBH I I', 1, 7, 0, packetSize, self.refId) + payload
    return result

