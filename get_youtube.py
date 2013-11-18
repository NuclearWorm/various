#!/usr/bin/env python

import urllib, sys, os, re

class GetYoutubeFlv():
  def __init__(self, url, filePath = '/tmp/youtube.flv'):
    self.url = url
    self.filePath = filePath
  
  def get_it(self):
    if not self.url:
      print "Give the url!\n\tExample: ./get_youtube.py URL filePath"
      sys.exit(1)  

    print "File will be stored as ", self.filePath
    
    if os.path.exists(self.filePath):
      try:
        last_m = os.stat(self.filePath).st_mtime
      except Exception, e:
        print "Was ERROR in getting info of %s:  %s!! FAILED!"%(self.filePath, str(e))
    else:
      last_m = 0
      
    get_youtube_url = 'http://youtube.com/get_video.php?'
    page = urllib.urlopen(self.url)
    
    path = re.compile('/watch_fullscreen\?(.*)plid=')
    line = page.readline()
    while line:  
      if path.search(line):
        params = path.search(line).groups()[0]
        break
      line = page.readline()
    else:
      print "File Path in the webpage was NOT found!!"
      sys.exit(1)
      
    try:
      urllib.urlretrieve(get_youtube_url + params, self.filePath)
    except Exception, e:
      print "Failed in saving file!! %s" % str(e)
      sys.exit(1)
    
    new_last_m = os.stat(self.filePath).st_mtime
    
    if os.path.exists(self.filePath) and last_m != new_last_m: print "Done!"
    else: print "File wasn't saved!"

def main(*args):
  try:
    url = args[0][1] 
  except:
    print "Give the url!\n\tExample: ./get_youtube.py URL FilePath"
    sys.exit(1) 

  try:
    file_name = args[0][2] 
  except:
    file_name = '/tmp/youtube.flv'
    pass
  
  
  print "Saving file to ................ %s"%file_name
  get_youtube = GetYoutubeFlv(url, file_name)
  get_youtube.get_it()

if __name__ == '__main__':
  main(sys.argv)

