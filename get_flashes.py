#!/usr/bin/env python

import urllib, sys, os, re

class GetFlashes():
  def __init__(self, filePath):
    self.filePath = filePath
    self.tmp_file = '/tmp/flashes'
  
  def run(self):
    def get_urls():
      if not self.filePath or not os.path.exists(self.filePath):
        print "Give the url!\n\tExample: ./get_youtube.py URL filePath"
        sys.exit(1)
      
      qik = re.compile('qik.com')
      pl_code = re.compile('(<object .*?</object>)', re.MULTILINE)
      
      results_dict = {}
      res_file = open(self.tmp_file, 'w')
      urls_file = open(self.filePath, 'r')
      urls = urls_file.readlines()
      for url in urls:
        try:
          page = urllib.urlopen(url).read()
          found = pl_code.search(page)
          if found:
            obj_code = found.groups()
            #print obj_code
            for i in obj_code:
              if qik.search(i):
                res_file.write('Object code from ' + str(url) + i + '\n')
                results_dict[i] = str(url)
        except Exception, e:
          print "With link %s was problem: "%str(url), str(e)
          pass
      urls_file.close()
      res_file.close()
    def uniq():
      link_re = re.compile('Object code from (.*?)\n')
      obj_re = re.compile('<object ')
      flashvars = re.compile('FlashVars="([^"]*?)"')
      flashvars1 = re.compile('http://qik.com/swfs/qik_player.swf\?streamname=STREAM_NAME&vid=VID_NUMBER&(.*?)"')
      
      results_dict = {}
      f = open(self.tmp_file, 'r')
      for line in f.readlines():
        if link_re.match(line):
          value = link_re.match(line).groups()[0]
        elif obj_re.match(line):
          results_dict[line] = value
      f.close()
      #print results_dict
      print len(results_dict)
      #for k, v in results_dict.iteritems():
      links = results_dict.keys()
      #for i in links:
      #  print i
      
      
      links1 = links
      links2 = []
      links3 = []
      t2 = open('/tmp/t2', 'w')
      t3 = open('/tmp/t3', 'w')
      for code in links1:
        new = re.sub('streamname=[\d\w]*?&', 'streamname=STREAM_NAME&', code)
        new = re.sub('user=[\d\w]*?&', 'user=USER&', new)
        new = re.sub('displayname=[\d\w]*?&', 'displayname=DISPLAYNAME&', new)
        new = re.sub('safelink=[\d\w_]*', 'safelink=SAFELINK', new)
        new = re.sub('vid=[\d]*?&', 'vid=VID_NUMBER&', new)
        new = re.sub('height="\d+"', 'height="HEIGHT"', new)
        new = re.sub('width="\d+"', 'width="WIDTH"', new)
        new = re.sub('swflash.cab#version=[\d,]+"', 'swflash.cab#version=V,E,R,S,I,O,N"', new)
        links2.append(new)         
        t2.write(new)

        if flashvars.search(new):
          links3.append(flashvars.search(new).groups()[0])
          t3.write(flashvars.search(new).groups()[0] + '\n')
        
        elif flashvars1.search(new):
          links3.append(flashvars1.search(new).groups()[0])
          t3.write(flashvars1.search(new).groups()[0] + '\n')
          
      t3.close()
      t2.close()
      t4 = open('/tmp/result.html', 'w')
      for l in set(links3):
        t4.write(l+'\n')
      t4.close()
      
      """links1 = links
      links2 = []
      links3 = []
      links4 = []
      
      obj = re.compile('(<object .*?>)')
      for code in links1:
        new = re.sub('streamname=[\d\w]*?&', 'streamname=STREAM_NAME&', code)
        new = re.sub('user=[\d\w]*?&', 'user=USER&', new)
        new = re.sub('displayname=[\d\w]*?&', 'displayname==DISPLAYNAME&', new)
        new = re.sub('safelink=[\d\w]*?&', 'safelink==SAFELINK&', new)
        new = re.sub('vid=[\d]*?&', 'vid==VID_NUMBER&', new)
        new = re.sub('height="\d+"', 'height="HEIGHT"', new)
        new = re.sub('width="\d+"', 'width="WIDTH"', new)
        new = re.sub('swflash.cab#version=[\d,]+"', 'swflash.cab#version=V,E,R,S,I,O,N"', new)
        links2.append(new)
        if obj.match(new):
          links3.append(obj.match(new).groups()[0])
      
      
      print len(links2)
      links4 = set(links2)
      print len(links4)
      for i in links4:
        print i
      print len(set(links3))
      for i in set(links3):
        print i
      #print links1
      """
      
      
    
    
    
    #get_urls()
    uniq()
    
    

def main(*args):
  try:
    file_name = args[0][1] 
  except:
    print "Give urls file as argument!"
    sys.exit(1)
        
      
      
  print "Reading URLS from ................ %s"%file_name
  get_flashes = GetFlashes(file_name)
  get_flashes.run()

if __name__ == '__main__':
  main(sys.argv)
