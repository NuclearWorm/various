import struct

PROTO_SIGNALLING = 5
PROTO_LOGGING    = 6
PROTO_MEDIA      = 7

def encodeIntElement(val, name):
  if val is None:
    return ''
  return struct.pack('!BHI', 0x03, name, val)  
def encodeShortElement(val, name):
  if val is None:
    return ''
  return struct.pack('!BHH', 0x02, name, val)  
def encodeByteElement(val, name):
  if val is None:
    return ''
  return struct.pack('!BHB', 0x01, name, val)  
def encodeUuidElement(val, name):
  if val is None:
    return ''
  hiword = val >> 64
  loword = val & 0xFFFFFFFFFFFFFFFF
  return struct.pack('!BHQQ', 0x05, name, hiword, loword)  
def encodeFlagElement(val, name):
  if not val:
    return ''
  return struct.pack('!BH', 0x00, name)  

def encodeStringElement(str, name):
  if str is None:
    return ''
  return struct.pack('!BHH', 0x10, name, len(str)) + str 

def encodeBlobElement(blob, name):
  if str is None:
    return ''
  return struct.pack('!BHH', 0x11, name, len(blob)) + blob 


def encodeTimeElement(val, name):
  if val is None:
    return ''
  return struct.pack('!BHQ', 0x08, name, val)  
