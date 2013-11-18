#!/usr/bin/env python
import os, sys, re, glob
import logging

LOG_FILENAME = '/tmp/compare_video.log'
logging.basicConfig(filename=LOG_FILENAME, filemode = 'w', level=logging.DEBUG,)

class CompareVideo:
  def __init__(self, vid1, vid2):
    self.video1 = vid1
    self.video2 = vid2
    self.tmp = '/tmp/'
    self.dir1 = self.tmp + 'dir1/'
    self.dir2 = self.tmp + 'dir2/'
    if not os.path.isdir(self.dir1): os.mkdir(self.dir1)
    if not os.path.isdir(self.dir2): os.mkdir(self.dir2)
    
    pass
  
  
  def compare(self):
    
    def extract(video_file, directory):
      logging.debug('Executing: ffmpeg -i ' + video_file + ' -r 1  -ss 00:00:00 -f image2 ' + directory + '/25frames_%05d.png 2>/tmp/errors')
      outp = os.system('ffmpeg -i ' + video_file + ' -r 1  -ss 00:00:00 -f image2 ' + directory + '25frames_%05d.png 2>/tmp/errors')
      logging.debug('def: extract ' + video_file + ' to ' + directory + '\nlist of files is ' + str(sorted(os.listdir(directory))) + '\nOutput is ' + str(outp))
      if outp != 0: print "FFmpeg returned not zero, but " + str(outp)
      return sorted(os.listdir(directory))

      pass
    
    def compare_img(image):
      logging.debug(image)
      result=[0,0,0]
      logging.debug("Executing: " + "compare " + self.dir1 + image + " " + self.dir2 + image + "  -verbose -metric AE null: 2>&1")
      outp = os.popen("compare " + self.dir1 + image + " " + self.dir2 + image + "  -verbose -metric AE null: 2>&1")
      output_cmp = outp.readlines()
      logging.debug("Got from compare:\n%s"%str(output_cmp))
      try:
        reg_data = [x for x in output_cmp if "all" in x][0]
      except Exception, e:
        if "image size differs" in str(output_cmp):
          return "Operation has failed: Image sizes are different, can't compare it!"
        else:
          return "Operation has failed: Unknown error when comparing images!\n%s"%str(e)
      result[0] = re.search('([\d\.]+)', reg_data).groups()[0]
      logging.debug('def: compare_img\nAE result is ' + str(result[0]))
      #if not outp.close(): logging.debug("def: compare_img\nCompare has been failed!")
      logging.debug("Executing: " + "compare " + self.dir1 + image + " " + self.dir2 + image + "  -verbose -metric MAE null: 2>&1")
      outp = os.popen("compare " + self.dir1 + image + " " + self.dir2 + image + "  -verbose -metric MAE null: 2>&1")
      reg_data = [x for x in outp.readlines() if "all" in x][0]
      result[1] = re.search('([\d\.]+) \(', reg_data).groups()[0]
      logging.debug('def: compare_img\nMAE result is ' + str(result[1]))
      #if not outp.close(): logging.debug("def: compare_img\nCompare has been failed!")
      logging.debug("Executing: " + "convert " + self.dir1 + image + " " + self.dir2 + image + " -compose difference -composite -colorspace gray miff:- | identify -verbose - ")
      outp = os.popen("convert " + self.dir1 + image + " " + self.dir2 + image + " -compose difference -composite -colorspace gray miff:- | identify -verbose - ")
      reg_data = [x for x in outp.readlines() if "mean:" in x][0]
      result[2] = re.search('([\d\.]+) \(', reg_data).groups()[0]
      logging.debug('def: compare_img\nConvert result is ' + str(result[2]))
      #if not outp.close(): logging.debug("def: compare_img\nCompare has been failed!")
      logging.debug('def: compare_img\nOverall result is ' + str(result))
      
      return result
      
      
      pass
    
    def print_result(images1):
      
      res = []
      logging.debug(images1)
      for image in images1:
        logging.debug("Working on " + str(image))
        tmp = compare_img(image)
        if 'Operation has failed' in tmp:
          if "Image sizes are different" in tmp:
            return "The files have different picture-size!! Can't compare it!\nError %s"%tmp
          else:
            return "There was error in comparing:\n%s"%tmp
        res.append(tmp)
        logging.debug("With result " + str(tmp))
      logging.debug(str(res))
      avg = []
      for i in range(0, 3):
        avg.append(sum([float(x[i]) for x in res])/len(res))
      logging.debug('List of averages' + str(avg))
      for item in res:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
          logging.debug("Frame on second %d is SAME"%(res.index(item) + 1))
      if avg[2] == 0:
        return "The files are SAME, coeff < 2"
      elif avg[2] <= 3:
        return "The files are very SIMILAR, coeff: %.2f\ngammas: %.2f, %.2f"%(avg[2], avg[0], avg[1])
      else:
        return "The files are DIFFERENT with coeff: %.2f\ngammas: %.2f, %.2f"%(avg[2], avg[0], avg[1])
      pass
      
    
  
    
    
    list_img1 = extract(self.video1, self.dir1)
    list_img2 = extract(self.video2, self.dir2)
    
    logging.debug('List of dir1:\n' + str(list_img1) + 'List of dir2:\n' + str(list_img2))
    if list_img2 == [] or list_img1 == []:
      print "Extract failed! No files!"
      sys.exit()
    if len(list_img1) < len(list_img2):  
      return print_result(list_img1)
    else: return print_result(list_img2)
    
    pass
  
  
  
  
  def simple_compare(self):
    
    
    
    
    
    pass
  
  def clean(self):
    logging.debug("Cleaning.................")
    for dirr in self.dir1, self.dir2:
      for fi in os.listdir(dirr): 
        os.remove(dirr + fi)
      #os.rmdir(dirr)
    logging.debug("After clean: \nDir 1:\n" + str(os.listdir(self.dir1)) + '\nDir 2:\n' + str(os.listdir(self.dir2)))
    pass



def main(*args):
  file1 = sys.argv[1]
  file2 = sys.argv[2]
  compare = CompareVideo(file1, file2)
  print compare.compare()
  compare.clean()
  
  pass
  
if __name__ =='__main__':
  main(sys.argv)
 
