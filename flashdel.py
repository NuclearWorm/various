#!/usr/bin/env python
import re, os, sys

import time

import fileinput



def main(*args):
    dump_file = "/tmp/dump"
    dump_tmp = "/tmp/dumptmp"
    dump = "/tmp/dump_p"
    html = '/tmp/qikbug_' + str(int(time.time())) + '.html'
    dbg = 1
    
    os.system("tshark -R http -T text -V -r " + dump_file + " > " + dump_tmp + "")
       
### Work on tcpdump text file

    t2 = open(dump, 'w')
    t2.write("Start\n")
    get = re.compile('\s+GET')
    post = re.compile('\s+POST')
    time_re = re.compile('\s+Arrival Time: [^:]*?:(\d+):(\d+)\.(\d{3})(\d{3})')
    http_rep = re.compile('\s+HTTP/1.1 \d+\s[\w\s]+')
    port = re.compile('Transmission Control Protocol, Src Port: [\d\w]+ \((\d+)\), Dst Port: [\w\d]+ \((\d+)\)')
    host = re.compile('\s+Host: .*')
    for line in fileinput.input(dump_tmp):
        #if 'GET' in line or 'POST' in line or 'Arrival Time:' in line:
        #    t2.write(line)
        times = time_re.match(line)
        ports = port.match(line)
        hosts = host.match(line)
        if get.match(line) or post.match(line):
            t2.write(line.replace('HTTP/1.1\\r\\n', ''))
        elif times:
            res = times.groups()
            timestamp = str(int(res[0])*60000 + int(res[1])*1000 + int(res[2]) + float(res[3])/1000)+'\n'
            t2.write(timestamp)
            #t2.write(''.join(time.match(line).groups())+'\n')
        elif http_rep.match(line):
            t2.write(line.replace('\\r\\n', '').replace('HTTP/1.1', ''))
        #elif 'Transmission Control Protocol' in line:
        #    t2.write(line)
        elif ports:
            res_p = ports.groups()
            t2.write(res_p[0] + ' - ' + res_p[1] + '\n')
        elif hosts:
            t2.write(line.replace('\\r\\n', ''))
    
    t2.close

    
    rdict = {}
    time_re = re.compile('^[\d\.]+$')
    port = re.compile('\d+ - \d+')
    port12 = re.compile('(\d+) - (\d+)')
    req = re.compile('\s*?[\w\d]+\s[\w/]+', re.I)
    getpost = re.compile('GET|POST')
    for line in fileinput.input(dump):
        if time_re.match(line):
            my_time = line.rstrip('\n')
            if dbg == 1: print 'Time: ' + line
            #rdict.setdefault(line,[])
        elif port.match(line):
            my_port = line.rstrip('\n')
            #port1 = port12.match(line).groups()[0]
            #port2 = port12.match(line).groups()[1]
            port1,port2 = port12.match(line).groups() 
            if dbg == 1: print 'Ports: ' + line
        elif req.match(line):
            if dbg == 1: print 'Request: "' + line + '"'
            req_cur = line.lstrip(' ').rstrip('\n')
            rdict[my_time] = [req_cur, port1, port2]
            if dbg == 1: print "Added to dictionary: " + str(req_cur) + ' - ' +  str(rdict[my_time]) + '\n'
            
        elif host.match(line):   
            req_cur = req_cur + ' --- ' + line.lstrip(' Host:').rstrip('\n')
            #rdict[my_time][0] = req_cur
            rdict[my_time] = [req_cur, port1, port2]
            if dbg == 1: print "Added to dictionary: " + str(req_cur) + ' - ' +  str(rdict[my_time]) + '\n'
            
    
    if dbg == 1: print rdict
    #for z in rdict:
    #    print z, rdict[z]
    #dict2 = sorted(rdict.items(), lambda x, y: cmp(int(x[1][0]), int(y[1][0])))
    if dbg == 1: print "+++++"*15
    #print dict2
    if dbg == 1: print "Request\tStart time\tPorts\tAnother\n"
    req = re.compile('GET|POST')
    port_s = re.compile('(\d+) - (\d+)')
    reply = re.compile('(\d+)\s(\w+)')
    times_1 = sorted(rdict.keys())
    for res in times_1:
        if dbg == 1: print 'Current time - %s'%res
        if req.match(rdict[res][0]):
            p1 = rdict[res][1]
            p2 = rdict[res][2]
            
            cur_pl = times_1.index(res)
            if dbg == 1: print '%d - current place, ports - %s - %s'%(cur_pl, p1, p2)
            for iter in range(cur_pl, len(times_1)):
                if reply.match(rdict[times_1[iter]][0]):
                    if dbg == 1: print "Found reply in time %s - %s, with ports %s - %s"%(times_1[iter], rdict[times_1[iter]][0], rdict[times_1[iter]][1], rdict[times_1[iter]][2])
                    if rdict[times_1[iter]][1] == p2 and rdict[times_1[iter]][2] == p1:
                        if dbg == 1: print 'Found same ports!!!'
                        stadium = float(times_1[iter]) - float(res)
                        rdict[res].append(stadium)
                        rdict[res].append(reply.match(rdict[times_1[iter]][0]).groups()[0])
                        if dbg == 1: print res, rdict[res]
                        break
                if iter == (len(times_1) - 1):
                    if dbg == 1: print 'Add zero!'
                    rdict[res].append(0)
                    rdict[res].append('n/a')
    new_dict = dict([(k, v) for k, v in rdict.iteritems() if req.match(v[0])])
    
    
    
    for h in rdict.items():
        if dbg == 1: print h
        if re.match(r'GET /swf', h[1][0]): print 'Found what you need!'
    if dbg == 1: print "+++++"*15
    start_time = 0
    start_req = re.compile('GET /\s')
    for h, v in new_dict.iteritems():
        if start_req.match(v[0]):
            start_time = float(h)
            if dbg == 1: print 'Found start time!!! %s - %s'%(h, v)
            break
    if dbg == 1: print "Start time is %d"%start_time
    if dbg == 1: print "+++++"*15
    for iter in sorted([x for x, y in new_dict.iteritems()]):
        if dbg == 1: print "Date: %d\t%s\t%s\t%d msec"%((int(float(iter) - start_time)), new_dict[iter][4], new_dict[iter][0], new_dict[iter][3])
    
    post = re.compile('POST')
    regs = (re.compile('GET /\s'), re.compile('POST /videos/played'), re.compile('GET /video/'), re.compile('GET /stream'), re.compile('GET /swf'))
    
    ht = open(html, 'w')
    ht.write("""<body><h1>HTTP statistics for loading qik webpage</h1>\n<table cellpadding="3" border=".5">\n
             <tr><td><h3>Start time</td><td><h3>HTTP reply</td><td><h3>HTTP request</td><td><h3>Time reply</td><td><h3>Time reply lines</td></tr>\n""")
    color = ['black', 'black', 'black', 'black', 'white']
    
    host_m = re.compile('.*?--- (.*)$')
    qik = re.compile('qik.com')
    for iter in sorted([x for x, y in new_dict.iteritems()]):
#########  Colorizing        
        color = ['black', 'black', 'black', 'black', 'white']
        if new_dict[iter][3] > 800: color[3] = 'red'
        if new_dict[iter][4] == '200': color[1] = 'green'
        else: color[1] = 'red'
        if post.match(new_dict[iter][0]): color[2] = 'blue'
        for reg in regs:
            if reg.match(new_dict[iter][0]): color[4] = 'yellow'
            if not qik.search(host_m.match(new_dict[iter][0]).groups()[0]): color[4] = 'mistyrose'
        ht.write("""<tr bgcolor="%s"><td><font color="%s">%d msec</font></td><td><font color="%s">%s</font></td><td><font color="%s">%s</font></td><td><font color="%s">%d msec</font></td>
                 <td align=left><img border=2 src="http://www.mountaindragon.com/html/reddot.gif" height=30 width=%d> </td></tr>"""%
                 (color[4], color[0], (int(float(iter) - start_time)), color[1], new_dict[iter][4], color[2], new_dict[iter][0], color[3], new_dict[iter][3], int(new_dict[iter][3]/4)))
        color = 'black'
    ht.write('</table></body>')
    ht.close



if __name__ == "__main__":
  main(sys.argv)