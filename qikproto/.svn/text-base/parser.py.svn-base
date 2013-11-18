import struct

ELEMENT_TYPE_FLAG    = 0
ELEMENT_TYPE_BYTE1   = 1
ELEMENT_TYPE_BYTE2   = 2
ELEMENT_TYPE_BYTE4   = 3
ELEMENT_TYPE_BYTE8   = 4
ELEMENT_TYPE_BYTE16  = 5
ELEMENT_TYPE_FLOAT   = 6
ELEMENT_TYPE_DOUBLE  = 7
ELEMENT_TYPE_TIME8   = 8
ELEMENT_TYPE_UTF8_16 = 0x10
ELEMENT_TYPE_UTF8_32 = 0x90
ELEMENT_TYPE_BLOB16  = 0x11
ELEMENT_TYPE_BLOB32  = 0x91
ELEMENT_TYPE_ESD16   = 0x12
ELEMENT_TYPE_ESD32   = 0x92
ELEMENT_TYPE_MAP16   = 0x13
ELEMENT_TYPE_MAP32   = 0x93


class Element(object):
  pass

class Packet(object):
  pass

class Parser(object):
  def __init__(self):
    self.buffer = str()
  def push(self, data):
    self.buffer = self.buffer + data
#    print 'buffered: %d'%len(self.buffer)
  def getPacket(self):
    packethdrformat = '>BBHII'
    pkthdrsize = struct.calcsize(packethdrformat)
    if len(self.buffer) >= pkthdrsize:
      pkthdr = struct.unpack(packethdrformat, self.buffer[:pkthdrsize])
      (version, protocol, opcode, pkt_len, ref_id) = pkthdr
      if pkt_len > pkthdrsize:
        payload = self.buffer[pkthdrsize:pkt_len]
#        print 'payload size is %d'%len(payload)
        elements = self.parsePacketPayload(payload)
#        print 'Parsed %d elements in packet'%len(elements)
      else:
        elements = []
      self.buffer = self.buffer[pkt_len:]
#      print 'Remaining in buffer: %d'%len(self.buffer)
      pkt = Packet()
      pkt.__dict__['version'] = version
      pkt.__dict__['protocol'] = protocol
      pkt.__dict__['ref_id'] = ref_id
      pkt.__dict__['opcode'] = opcode
      pkt.__dict__['elements'] = elements
      return pkt

  def parsePacketPayload(self, payload):
    elhdrfmt = ">BH"
    elhdrsize=struct.calcsize(elhdrfmt)
    elementList = []
    while len(payload) > 0:
      elhdr = payload[0:elhdrsize]
      payload = payload[elhdrsize:]
      (type, name) = struct.unpack(elhdrfmt, elhdr)
      
      structElement = Element()
      structElement.__dict__["name"]=name
#      structElement = {"nodetype":"ELEMENT", "name": "0x%04X"%name}
#      if (proto==5) and name in SignallingElementName:
#        structElement["name-sym"]=SignallingElementName[name]
#      if (proto==7) and name in MediaElementName:
#        structElement["name-sym"]=MediaElementName[name]
      
      if type == ELEMENT_TYPE_FLAG:
#        print "0x%04X : FLAG"%name
        structElement.__dict__["type"]="FLAG"
        structElement.__dict__["value"]=True
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_BYTE1:
        eldatafmt = ">B"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
#        structElement["type"]="BYTE1"
#        structElement["value"] = elval[0]
        structElement.__dict__["type"]="BYTE1"
        structElement.__dict__["value"]=elval[0]
#       context.putElement(structElement)
      elif type == ELEMENT_TYPE_BYTE2:
        eldatafmt = ">H"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
#       structElement["type"]="BYTE2"
#       structElement["value"] = elval[0]
        structElement.__dict__["type"]="BYTE2"
        structElement.__dict__["value"]=elval[0]
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_BYTE4:
        eldatafmt = ">I"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        structElement.__dict__["type"]="BYTE4"
        structElement.__dict__["value"]=elval[0]
#        structElement["type"]="BYTE4"
#        structElement["value"] = elval[0]
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_BYTE8:
        eldatafmt = ">Q"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        structElement.__dict__["type"]="BYTE8"
        structElement.__dict__["value"]=elval[0]
#        structElement["type"]="BYTE8"
#        structElement["value"] = elval[0]
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_BYTE16:
        eldatafmt = ">QQ"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        structElement.__dict__["type"]="BYTE16"
        structElement.__dict__["value"]=elval
#        structElement["type"]="BYTE16"
#        structElement["value"] = "0x%016X%016X"%elval
  #      context.putElement({"nodetype":"ELEMENT", "type":"BYTE16", "name":"0x%04X"%name, "value" : "0x%016X%016X"%elval})
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_FLOAT:
        print "0x%04X : FLOAT"%name
      elif type == ELEMENT_TYPE_DOUBLE:
        print "0x%04X : DOUBLE"%name
      elif type == ELEMENT_TYPE_TIME8:
        eldatafmt = ">Q"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        structElement.__dict__["type"]="TIME8"
        structElement.__dict__["value"]=elval[0]
#        structElement["type"]="TIME8"
#        structElement["value"] = elval[0]
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_UTF8_16:
        eldatafmt = ">H"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        str_len = elval[0]
        eldatafmt = "%ds"%str_len
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
  #      print "0x%04X : UTF8-short, len=%db \"%s\""%(name, str_len, elval[0])
  #      context.putElement({"nodetype":"ELEMENT", "type":"UTF8-short", "name":"0x%04X"%name, "length": str_len, "value" : elval[0]})
#        structElement["type"]="UTF8-short"
#        structElement["length"]= str_len
#        structElement["value"] = elval[0]
        structElement.__dict__["type"]="UTF8"
        structElement.__dict__["value"]=elval[0]
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_UTF8_32:
        eldatafmt = ">I"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        str_len = elval[0]
        eldatafmt = "%ds"%str_len
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
  #      print "0x%04X : UTF8-long, len=%db \"%s\""%(name, str_len, elval[0])
  #      context.putElement({"nodetype":"ELEMENT", "type":"UTF8-long", "name":"0x%04X"%name, "length": str_len, "value" : elval[0]})
        structElement.__dict__["type"]="UTF8"
        structElement.__dict__["value"]=elval[0]
#        structElement["type"]="UTF8-long"
#        structElement["length"]= str_len
#        structElement["value"] = elval[0]
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_BLOB16:
        eldatafmt = ">H"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        blob_len = elval[0]
        blob_data = payload[0:blob_len]
        payload = payload[blob_len:]
  #      print "0x%04X : BLOB16, len=%d"%(name,blob_len)
  #      context.putElement({"nodetype":"ELEMENT", "type":"BLOB16", "name":"0x%04X"%name, "length": blob_len, "data":byteStringToHex(blob_data)})
        structElement.__dict__["type"]="BLOB16"
        structElement.__dict__["value"]=blob_data
#       structElement["type"]="BLOB16"
#        structElement["length"]= blob_len
#        structElement["value"] = byteStringToHex(blob_data)
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_BLOB32:
        eldatafmt = ">I"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        blob_len = elval[0]
        blob_data = payload[0:blob_len]
        payload = payload[blob_len:]
  #      print "0x%04X : BLOB32, len=%d"%(name,blob_len)
  #      context.putElement({"nodetype":"ELEMENT", "type":"BLOB32", "name":"0x%04X"%name, "length": blob_len})
        structElement.__dict__["type"]="BLOB32"
        structElement.__dict__["value"]=blob_data
#        structElement["type"]="BLOB32"
#        structElement["length"]= blob_len
#        structElement["value"] = byteStringToHex(blob_data)
#        context.putElement(structElement)
      elif type == ELEMENT_TYPE_ESD16:
        print "0x%04X : ESD16"%name
      elif type == ELEMENT_TYPE_ESD32:
        print "0x%04X : ESD32"%name
      elif type == ELEMENT_TYPE_MAP16:
        eldatafmt = ">H"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        map_len = elval[0]      
        map_payload = payload[0:map_len]
        payload = payload[map_len:]
  #      context.startElement({"nodetype":"ELEMENT", "type":"MAP16", "name":"0x%04X"%name, "length": map_len})
        structElement["type"]="MAP16"
        structElement["length"]= map_len
        context.startElement(structElement)
        parsePacketPayload(proto, map_payload, context)
        context.endElement()
      elif type == ELEMENT_TYPE_MAP32:
        eldatafmt = ">I"
        eldatasize = struct.calcsize(eldatafmt)
        elval = struct.unpack(eldatafmt, payload[0:eldatasize])
        payload = payload[eldatasize:]
        map_len = elval[0]      
        map_payload = payload[0:map_len]
        payload = payload[map_len:]
  #      context.startElement({"nodetype":"ELEMENT", "type":"MAP32", "name":"0x%04X"%name, "length": map_len})
        structElement["type"]="MAP32"
        structElement["length"]= map_len
        context.startElement(structElement)
        parsePacketPayload(proto, map_payload, context)
        context.endElement()
      else:
        print "0x%04X : 0x%02X"%(name,type)
      elementList.append(structElement)
    return elementList
  