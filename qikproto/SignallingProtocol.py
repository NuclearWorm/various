import struct

from presentation import encodeIntElement, encodeShortElement, encodeByteElement, encodeUuidElement, encodeFlagElement, encodeStringElement, encodeTimeElement

OPCODE_SESSION_START             = 0x0000
OPCODE_SESSION_END               = 0x0001
OPCODE_STREAM_START              = 0x0002
OPCODE_STREAM_END                = 0x0003
OPCODE_STREAM_ATTRIBUTES         = 0x0004
OPCODE_DEVICE_REPORT             = 0x0005
OPCODE_UPDATE_AVAILABLE          = 0x0006
OPCODE_ACTIVATE                  = 0x0007
OPCODE_PING                      = 0x0008
OPCODE_GENERIC_MESSAGE           = 0x0009
OPCODE_STREAM_STATS              = 0x000A
OPCODE_DELIVERY_REPORT_REQUEST   = 0x000B
OPCODE_FILE_START                = 0x000C
OPCODE_FILE_STOP                 = 0x000D
OPCODE_ADD_ASSET_TO_EDIT         = 0x000E
OPCODE_ANONYMOUS_GENERIC_MESSAGE = 0x0010
OPCODE_INVALIDATE_SHORT_IDS      = 0x0011

OPCODE_RES_OK                    = 0x8000
OPCODE_RES_AUTH_FAILED           = 0x8001
OPCODE_RES_UPDATE_REQUIRED       = 0x8002
OPCODE_RES_STREAM_DOES_NOT_EXIST = 0x8003
OPCODE_RES_INVALID_PROTOCOL      = 0x8004
OPCODE_RES_INVALID_OPCODE        = 0x8005
OPCODE_RES_MALFORMED_PACKET      = 0x8006
OPCODE_RES_REQUEST_UNEXPECTED    = 0x8007 
OPCODE_RES_SERVER_ERROR          = 0x8008 
OPCODE_RES_ACTIVATION_FAILED     = 0x8009
OPCODE_RES_SERVER_BUSY           = 0x800A


  #elements
ELEMENT_DEVICE_ID                 = 0x0000 # UTF8
ELEMENT_USER_PHONE                = 0x0001 # UTF8
ELEMENT_USER_CODE                 = 0x0002 # UTF8
ELEMENT_CLIENT_SW_VERSION         = 0x0003 # UTF8
ELEMENT_CLIENT_PLATFORM           = 0x0004 # UTF8
ELEMENT_CLIENT_DNLOAD_URL         = 0x0005 # UTF8
ELEMENT_GENERIC_PARAM             = 0x0006 # MAP
ELEMENT_SESSION_UUID              = 0x0007 # BYTE16
ELEMENT_CLIENT_APP_CYCLE          = 0x0008 # BYTE4 
ELEMENT_CLIENT_CAPS               = 0x0009 # BYTE4
ELEMENT_SERVER_CAPS               = 0x000A # BYTE4
ELEMENT_DEVICE_UNIQUE_STRING      = 0x000B # UTF8
ELEMENT_USER_NAME                 = 0x000C # UTF8
ELEMENT_DONT_INVALIDATE_SHORT_IDS = 0x000D # FLAG
ELEMENT_DEVICE_MODEL              = 0x000E # UTF8, 50 symbols max
ELEMENT_NEGOTIATED_CAPS           = 0x000F # BYTE4
  
ELEMENT_STREAM_IDX                = 0x0010 # BYTE1
ELEMENT_STREAM_UUID               = 0x0011 # BYTE16
ELEMENT_TRANSMITTER_TIME          = 0x0012 # BYTE8
ELEMENT_TRANSMITTER_TZ            = 0x0013 # BYTE1
ELEMENT_STREAM_ATTRIBUTE          = 0x0014 # BYTE1
ELEMENT_NOT_LIVE_STREAM           = 0x0015 # FLAG
ELEMENT_STREAM_STATS              = 0x0016 # STRUCTURE
ELEMENT_STREAM_VIEWERS            = 0x0017 # BYTE1 | BYTE2 | BYTE4
ELEMENT_STREAM_DELIVERY_REPORT    = 0x0018 # BLOB
ELEMENT_STREAM_PAUSE              = 0x0019 # FLAG, used in STREAM_STOP, FILE_UPLOAD_STOP
ELEMENT_CONTENT_TYPE              = 0x001A #
ELEMENT_SHORT_ASSET_ID            = 0x001B # Client-assigned assetId (streamId) 
ELEMENT_FILE_NAME                 = 0x001C # UTF8
  
ELEMENT_VIDEO_CODEC               = 0x0020 # BYTE4
ELEMENT_VIDEO_HSIZE               = 0x0021 # BYTE4
ELEMENT_VIDEO_VSIZE               = 0x0022 # BYTE4
ELEMENT_VIDEO_CLOCK_NUM           = 0x0023 # BYTE4
ELEMENT_VIDEO_CLOCK_DENUM         = 0x0024 # BYTE4

ELEMENT_AUDIO_CODEC               = 0x0030 # BYTE4
ELEMENT_AUDIO_CLOCK_NUM           = 0x0033 # BYTE4
ELEMENT_AUDIO_CLOCK_DENUM         = 0x0034 # BYTE4
  
ELEMENT_IM_TEXT                   = 0x0040 # UTF8
ELEMENT_IM_AUTHOR                 = 0x0041 # UTF8
ELEMENT_IM_DATE                   = 0x0042 # TIME8
  
ELEMENT_EDIT_UUID                 = 0x0050 # BYTE16



class SessionStartPacket(object):
  def __init__(self, deviceId, refId=0):
    self.deviceId = deviceId
    self.platform = "1"
    self.version ="0.0.1"
    self.refId = refId
  def getBytes(self):
    payload = (encodeStringElement(self.deviceId, ELEMENT_DEVICE_ID) + 
              encodeStringElement(self.platform, ELEMENT_CLIENT_PLATFORM) +  
              encodeStringElement(self.version, ELEMENT_CLIENT_SW_VERSION)) 
    packetSize = 12 + len(payload)
#    print 'Packet size: %d'%packetSize
    result = struct.pack('!BBH I I', 1, 5, OPCODE_SESSION_START, packetSize, self.refId) + payload
    return result

class StreamStartPacket(object):
  def __init__(self, refId=1, live=True,uuid = None, shortId = None, idx=0, vcodec=0, width=320, height=240, vc_num=1, vc_denum=1000, acodec=0, ac_num=1, ac_denum=8000):
    self.refId   = refId
    self.live    =live
    self.uuid    = uuid
    self.shortId = shortId
    self.idx     = idx
    self.vcodec  = vcodec 
    self.width   = width
    self.height  = height
    self.vc_num  = vc_num
    self.vc_denum= vc_denum
    self.acodec  = acodec 
    self.ac_num  =ac_num
    self.ac_denum=ac_denum
  def getBytes(self):
    payload = ( encodeByteElement(self.idx, ELEMENT_STREAM_IDX) +
                encodeUuidElement(self.uuid, ELEMENT_STREAM_UUID) + 
                encodeShortElement(self.shortId, ELEMENT_SHORT_ASSET_ID) +
                encodeFlagElement(not self.live, ELEMENT_NOT_LIVE_STREAM) +
                encodeTimeElement(0, ELEMENT_TRANSMITTER_TIME) +
                encodeIntElement(self.vcodec, ELEMENT_VIDEO_CODEC) + 
                encodeIntElement(self.width, ELEMENT_VIDEO_HSIZE) + 
                encodeIntElement(self.height, ELEMENT_VIDEO_VSIZE) + 
                encodeIntElement(self.vc_num, ELEMENT_VIDEO_CLOCK_NUM) + 
                encodeIntElement(self.vc_denum, ELEMENT_VIDEO_CLOCK_DENUM) + 
                encodeIntElement(self.acodec, ELEMENT_AUDIO_CODEC) + 
                encodeIntElement(self.ac_num, ELEMENT_AUDIO_CLOCK_NUM) + 
                encodeIntElement(self.ac_denum, ELEMENT_AUDIO_CLOCK_DENUM)  
              )
    packetSize = 12 + len(payload)
#    print 'Packet size: %d'%packetSize
    result = struct.pack('!BBH I I', 1, 5, OPCODE_STREAM_START, packetSize, self.refId) + payload
    return result

class StreamStopPacket(object):
  def __init__(self, refId=2, idx=0):
    self.refId   = refId
    self.idx     = idx
  def getBytes(self):
    payload = ( encodeByteElement(self.idx, ELEMENT_STREAM_IDX) +
                encodeTimeElement(0, ELEMENT_TRANSMITTER_TIME) 
              )
    packetSize = 12 + len(payload)
#    print 'Packet size: %d'%packetSize
    result = struct.pack('!BBH I I', 1, 5, OPCODE_STREAM_END, packetSize, self.refId) + payload
    return result

class SessionEndPacket(object):
  def __init__(self, refId=3):
    self.refId   = refId
  def getBytes(self):
    packetSize = 12
#    print 'Packet size: %d'%packetSize
    result = struct.pack('!BBH I I', 1, 5, OPCODE_SESSION_END, packetSize, self.refId)
    return result


