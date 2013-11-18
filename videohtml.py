#!/usr/bin/env python
 
import os, sys, glob, re
 
 
 
def main(*args):
  
  def return_embed(stream_name):
    return """<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
                            codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,115,0" width="425" height="319"
                            id="qikPlayer" align="middle"><param name="allowScriptAccess" value="always" /><param name="allowFullScreen" value="true"/>
                            <param name="movie" value="http://stage.qik.com/swfs/qikPlayer4.swf" /><param name="quality" value="high"/> 
                            <param name="bgcolor" value="#333333" /><param name="FlashVars" 
                            value="rssURL=http://stage.qik.com/video/""" + stream_name + """.rss&autoPlay=false&polling=false"/>
                            <embed src="http://stage.qik.com/swfs/qikPlayer4.swf" quality="high" bgcolor="#333333" width="425" height="319" 
                            name="qikPlayer" align="middle" allowScriptAccess="always" allowFullScreen="true" type="application/x-shockwave-flash"
                            pluginspage="http://www.macromedia.com/go/getflashplayer" 
                            FlashVars="rssURL=http://stage.qik.com/video/""" + stream_name + """.rss&autoPlay=false&polling=false" /></object>"""
 
    
  def get_bps(ofile):
    bitrate = os.popen("mediainfo " + ofile + " | grep 'Bit rate' | grep -v 'mode'").readlines()
    bitrate = bitrate[0].split(':')[1].lstrip()
    bitrate = bitrate.split()[0]
    return bitrate
  
  def get_qual(qual):
    if qual == 'bas': return "Basic"
    elif qual == 'med': return "Medium"
    elif qual == 'high': return "High"
    else: return "Unknown"
  
  def get_duration(ofile):
    duration = os.popen("mediainfo " + ofile + " | grep 'Duration'").readlines()
    duration = duration[0].split(':')[1].lstrip()
    #duration = duration.split()[0]
    return duration
  
  def get_info(file):
    return os.popen("mediainfo " + file).read()
  
  
  defdir = "/home/lupus/testools/testscripts/"
  origvideo_dir = defdir + '../origvideo/'
  encoded_dir = defdir + '../video/'
  streams = [
'3304f4cc8dc14eb4aee8a168845649c7.1',
'eef80e78b0f14955baf98eed0d3db389.1',
'98dfcffc7cc6492a87ce3383858f65f0.1',
'57eab1e5394043298938acceee2a7e68.1',
'4f3e021ad6ed4dd3b320661e5ddd3e11.1',
'a8a8b9f9e54145358da7d651e872cc3d.2',
'9342b8d1a7b0405a8dd3a37153a97f42.1',
'd80a47202e6240d488e29ef46c986b61.1',
'f2bc80997afe44f18a675e6608b3de41.1',
'7ab4e102f0bb4abebffda97edc98ad85.1',
'1ab4fabec225475395f620c3f339fee6.1',
'56c6153bc734475392180cc126d1dd67.1',
'c85c67dc576147a68a517988c06ecde7.1',
'c4133e7a538946f68d60e18da9c97314.1',
'e716be1207504670aed3ee14fea0f7c4.1',
'153220b1c03a4ffaae1982c1cd8a91f8.1',
'94533f80f710498d87126d1ff7e67ab9.1',
'418ea2da8dcb4e99a21cbc50837795fe.1',
'025c63298a4a465c92c5a0b63a11cd8b.1',
'5e8a0df5fc64414f88fa78b7ae08889a.1',
'53b5c16a35794444a6552be64621e69a.1',
'1e7f1245e8564d28a74fa30e6a34383c.1',
'abefe5f5ab9a43d6b32813c15ad58c6a.1',
'7aaaa0ae9b134c59a64f239dbe3087ed.1',
'47ddfeb2fe584cf691a9b51d757d21e3.1',
'703830e434bb4e68ab5f09ea51c94b2b.1',
'dba993d162fb4fd7a4bb2ce92f240065.1',
'01f008022ab04b9c94b5126ff8267cbb.1',
'2c2d95a31bb34b78836c3536e544fe96.1',
'd5f457ec843245de95800944bb990aad.1',
'63b8d02211f043aa954e9e47c48210f2.1',
'9211952ab6334091ab9b4531f4b49aa4.1',
'6877d631d27844b99ca90ac1bd6ff21a.1',
'd7cfb08f0980402e9c250e0c527ae569.1',
'c8cfb1a47c404ce3889fdd74ea3d9bfd.1',
'f019bbabe16b4024bcc10ec16ce41711.1',
'20259509cd7f4f4eb9031c0c8a28d90c.1',
'40453968d29e470f9a8823623ee4df78.1',
'3fb272ff6b854e70ae1310f051e9e8a5.1',
'de21c25d82b14aa0bc4f05f97aa40ed6.1',
'94a33674ed18435f89abf8159613e66c.1',
'f6cb3b89aa1c4b6fa7c0761b9c6fd066.1',
'd058172623a548cd9c526a4edaf4c426.1',
'b2d4cf443285445f907b76eefdfb4d97.1',
'397fb4c2513d42d3bc99e854bbb3daa7.1',
'6636e42f100745cab3c4535e02f9c6d2.1',
'3a3de307da574af6ac6d148356461a56.1',
'e659b2cf571e4fdaa2b5e16772538581.1',
'78b13d4ef8984b00aaf6cde71dd871a6.1',
'19fb69df64b24edc97f48b769705a26e.1',
'2583cbf126a44e009c2b7ba5aec59ade.1',
'71c72b2291c94c74a1e3d8ae42552a07.1',
'8d0403597f9e4e51a3d968560776cb72.2',
'bb99e71c2dee4c90984c19f9431578eb.1',
'7f6c123fdee54123b1d009df23129bd4.1',
'11bc9698a93b4f2f8658d57af3256780.1',
'4bb3209fb8da4d38b9cea4ab772177a9.1',
'939852ab4dc649f9b5d238541b0d8a5b.1',
'9822f5bb638842beb43d417de0def2f5.4',
'7c7069d95a3e4af881b5e8ae18c4c94d.1',
'6eff0d2ac4314748a88bce9c232e3a49.1',
'f7f29ff85b554b969ff389377b4886f6.1',
'cc18a1be24a84c9bb1d93b9f2812f3d9.1',
'3724741dac3d4d63970440ccae4dd637.1',
'502e17a709ed467393ec05b6f3320acc.1',
'a93d07057dfe49a0b6b109e9ca16a8e1.1',
'9e051913794a4ae9a5c49efa43410506.1',
'1004de3db7a64e608d386c9a122a5222.1',
'4e46781b857f43efbb76306feceb6135.1',
'c6ed849012ba4f358c300c2c1523ffcb.1',
'ee7cfdc9f4d04850b1c40c7e1f2ce9d1.1',
'69b3fd9f496c470f88fb012ff73e09ca.1',
'1aa278aa825d4135a22d9107a0f95273.1',
'afa82475a534478587a01382fba85f56.1',
'd9c1a5f677364152b2ff7ad75df66f6c.1',
'39504ffa0bf1483f8a6de8bae6b19353.1',
'de7f08791efb4faab4a80d00fa4b6761.1',
'a65912b41bca4ecf871bfd3f6b111f15.1',
'a10f99e5cb25437c932424c0d85cade0.1',
'088436eacdbe45dc8fa1bc31dd4153b3.1',
'f89d3313a4624924890d8f1364cac3d7.1',
'e6760adbd5ac4ddc850b2bc61c694ce6.1',
'6330d46934f845959b94c23dad73918a.1',
'8916d1e78114436a93ab473c42b62c76.1',
'6e9a60f2d4f5418bbb45cf390f27f437.1'  
  ]
  
  origingfo = {
    "320x240_30fps_mpeg4.mp4":[],
    "HTC_176x144_30fps_mpeg4.mp4":[],
    "HTC_320x240_30fps_mpeg4.mp4":[],
    "HTC_352x288_30fps_mpeg4.mp4":[],
    "HTC_352x288_6fps_mpeg4.mp4":[],
    "Nokia_176x144_bas.3gp":[],
    "Nokia_176x144_high.3gp":[],
    "Nokia_176x144_med.3gp":[],
    "Nokia_352x288_bas.3gp":[],
    "Nokia_352x288_high.3gp":[],
    "Nokia_352x288_med.3gp":[],
    "Nokia_640x280_bas.3gp":[],
    "Nokia_640x280_high.3gp":[],
    "Nokia_640x280_med.3gp":[]
  }
  samples = ['0.5', '0.7', '0.9', '1.1', '1.3', '1.5']
  
  """
  try:
    file_name = args[0][1] 
  except:
    print "Give the filename base!"
    sys.exit(1)
        
  files = glob.glob(file_name+'*')
  print files, len(files)
  #sys.exit(0)
  
  parser = re.compile('_([^_]+)_([0-9]+)br.flv')    
  
  
  
  tex = open('report', 'w')
  i = 0
  for f in files:
    try:
      os.system("\cp "+f+" /qfs/var/media.hq.flv/" + streams[i] + ".flv ")
    except Exception, e:
      print "Exception!! :: ", str(e)
      sys.exit()
    tex.write(f+ " - " + streams[i] + "
")
    i = i + 1
  tex.close()
  """
  
  rep = open(defdir + 'report', 'r')
  htc = re.compile('HTC_([0-9x]+)_([0-9]+)fps_mpeg4_([0-9]+)br.flv')
  nokia = re.compile('Nokia_([0-9x]+)_([a-z]+)_([0-9]+)br.flv')
  noname = re.compile('([0-9x]+)_([0-9]+)fps_mpeg4_([0-9]+)br.flv')
  flv = re.compile(' - ([a-z0-9.]+)$')
  arr = rep.readlines()
  base1 = re.compile('(\w+)\.(\w+)')
  
  for key in origingfo.keys():
    printed = {}
    tfile = open(defdir + '../tmp/' + key + '.html', 'w')
    tfile.write('<html><body>\n<h1 align=center>List of devices and flash players</h1>\n<h2>' + key + '</h2>\n')
    tfile.write("""
      <!-- <style>
      .visibleClass { visibility: visible }
      .hiddenClass { visibility: hidden }
      .blockClass { display: block }
      .noneClass { display: none }
      </style>
      <script>
      function setClass(id, styleClass) {
      document.getElementById(id).className = styleClass;
      //  alert(style);
      }
      </script>-->
      <style type="text/css"> 
      #col1 { width: 49%; float: left; }
      #col2 { width: 49%; float: right; }
      .hidden { display: none; }
      .unhidden { display: block; }
      </style>
      <script type="text/javascript">
      function unhide(divID) {
          var item = document.getElementById(divID);
          if (item) {
              item.className=(item.className=='hidden')?'unhidden':'hidden';
          }
      }
      </script>
      """)
    
    tfile.write("""<hr><p><a href="javascript:unhide('""" + key +  """');">Show original file Media Info</a>
                <br><div id='""" + key  + """' class="hidden">
                <pre>""" + get_info(origvideo_dir + key) + """</pre></div><br></p><hr><br><br> """)
    
    
    
    file_base = base1.match(key).groups()[0]
    enc_files = glob.glob(encoded_dir + file_base+'*')
    if enc_files == []: sys.exit(0)
    for efile in enc_files:
      sh_efile = re.search('.*/([\w\.]+)$', efile).groups()[0]
      for i in arr:
        if sh_efile in i: flv_file = flv.search(i).groups()[0]
      player_code = return_embed(flv_file.split('.')[0])
      ### Get info about every file
      #resol = get_resol()
      if "Nokia" in sh_efile:
        resol, qual, h_bitr = nokia.match(sh_efile).groups()
        fps = 'Unknown'
      elif "HTC" in sh_efile:
        resol, fps, h_bitr = htc.match(sh_efile).groups()
        qual = "Unknown"
      else:
        resol, fps, h_bitr = noname.match(sh_efile).groups()
      orig_bitr = get_bps(origvideo_dir + key)
      r_bitr = get_bps(efile)
      coeff1 = float(r_bitr)/float(orig_bitr)
      coeff2 = float(h_bitr)/float(orig_bitr)
      
      class_html = sh_efile.split('.')[0]
      #if "Nokia" in sh_efile:
        
      output = "%s<br>Resolution: %s<br>FPS: %s<br>Quality on phone: %s<br>Original bitrate: %s Kbps<br>Planned output bitrate: %s Kbps (%.3f of original)<br>Real bitrate: %s Kbps (%.3f of original)<br>\n"\
                  %(sh_efile,resol, fps, get_qual(qual), orig_bitr, h_bitr, coeff2, r_bitr, coeff1)
      output += """<a href="javascript:unhide('""" + class_html +  """');">Show Media Info</a>
                      <br><div id='""" + class_html  + """' class="hidden">
                    <pre>""" + get_info(efile) + """</pre></div><br><br> """
      output += "<br>%s<br></p>"%player_code
      printed[h_bitr] = output
      
    ii = 0  
    for br in sorted(printed.keys()):
      tfile.write('<br><hr align=center><br><p><b><big>Transcoder ratio: %s</big></b><br>'%samples[ii] + printed[br])
      ii +=1
    
    
    tfile.write('</body></html>')
    tfile.close()

  rep.close()
 
if __name__ =='__main__':
  main(sys.argv)
 
