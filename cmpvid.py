#!/usr/bin/env python

import logging, re, os, sys, glob
from comparevideo import CompareVideo

LOG_FILENAME = '/tmp/video_cmp.log'
logging.basicConfig(filename=LOG_FILENAME, filemode = 'w', level=logging.DEBUG,)

def main(*args):
  maindir = '/tmp/video/'
  result_file = open('/tmp/res.html', 'w')
  for file in glob.glob(maindir + '*'):
    try: file1 = re.search('/([\w]+)\.', file).groups()[0]
    except:
      print "Not found :)"
      continue
    if file1 != '':
      result_file.write('<br><hr><br>')
      for file2 in glob.glob(maindir + 'encoded/' + file1 + '*'):
        logging.debug("File1 is %s, file2 is %s, and file is %s"%(file1, file2, file))
        result_file.write("<p>File %s compare to file %s"%(re.search('/([\w]+\.[\w]+$)', file).groups()[0], re.search('/([\w]+\.[\w]+$)', file2).groups()[0]))
        cmp = CompareVideo(file, file2)
        return_func = cmp.compare()
        logging.debug("Added to file: <p>" + return_func)
        result_file.write('<p>' + return_func)
        cmp.clean()
  result_file.close()  


if __name__ =='__main__':
  main(sys.argv)
 