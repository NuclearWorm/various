#!/usr/bin/env python
import sys, os
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure, show, savefig
#import pylab as PyLab
import numpy as np
import matplotlib.pyplot as plt

def create_html(self):
    html_file = '/tmp/qik_delay.html'
    f = open(html_file, 'w')
    pic_files= [x for x in os.listdir('/tmp/') if 'filepic_' in x]
    f.write('<body>')
    for x in reversed(sorted(pic_files)):
        f.write('<img src="' + str(x) + '"><br>\n')
    f.write('</body>')
    f.close
    

###############
def main(*args):
    dict1 = {}
    for line in open('/tmp/dict1'):
        time_v, val = line.split(':',2)[:2]
        dict1.setdefault(time_v, []).append(val.rstrip())
    #print dict1
    dict2 = sorted(dict1.items(), lambda x, y: cmp(float(x[0]), float(y[0])))
    
    ###############
    fig = plt.figure(figsize=(13,7))
    ax = fig.add_subplot(111)
    #t = (0, 264.821, 319.096, 656.148, 746.605)
    s = [1]*len(dict2)
    t = [float(k) for k, v in dict2]
    #print t
    #print s
    line, = ax.plot(t, s, 'go-', label='Timeline', linewidth=2)
    position = (.25, .5, 1.5, 1.75)
    i_position = 0
    for k, v in dict2:
        key = float(k)
        val_text = str(v).strip('][,\'')
        key_text = str(key)
        i_position = i_position + 1
        if i_position == 4:
            i_position = 0
        #print position[i_position]
        #if (pos == 1.5):
        #    pos = .5
        #elif (pos == .5):
        #    pos = 1.5
        ax.annotate(val_text+"\n" + key_text +' msec', xy=(key, 1), xytext=(key-60, position[i_position]), xycoords='data', arrowprops=dict(facecolor='black', shrink=0.08),
                )
    """
    ax.annotate('GET/', xy=(t[0], 1), xytext=(1, 1.5), xycoords='data', arrowprops=dict(facecolor='black', shrink=0.08),
                )
    ax.annotate('GET RSS file\n'+str(t[1])+' msec', xy=(t[1], 1), xytext=(t[1]-60, 1.5), xycoords='data', arrowprops=dict(facecolor='black', shrink=0.08, width=0.5, headwidth=4),
                )
    ax.annotate('GET /swfs/qikPlayer4.swf\n'+str(t[2])+' msec', xy=(t[2], 1), xytext=(t[2]-60, .5), xycoords='data', arrowprops=dict(facecolor='black', shrink=0.08, width=0.5, headwidth=4),
                )
    ax.annotate('POST /videos/played\n'+str(t[3])+' msec', xy=(t[3], 1), xytext=(t[3]-60, 1.5), xycoords='data', arrowprops=dict(facecolor='black', shrink=0.08, width=0.5, headwidth=4),
                )
    ax.annotate('GET /swfs/qikPlayer4.swf\n'+str(t[4])+' msec', xy=(t[4], 1), xytext=(t[4]-50, .5), xycoords='data', arrowprops=dict(facecolor='black', shrink=0.08, width=0.5, headwidth=4),
                )
                """
    ax.set_ylim(0,2)
    #plt.show()
    
    """
    plt.savefig("/tmp/filepic.png", dpi=None, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False)
    """
    plt.savefig("/tmp/filepic.png")


if __name__ == "__main__":
  main(sys.argv)
  create_html(sys.argv)