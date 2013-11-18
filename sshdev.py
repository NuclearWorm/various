#!/usr/bin/env python

import logging
import ssh, sys, os

LOG_FILENAME = '/tmp/sshdev.log'
logging.basicConfig(filename=LOG_FILENAME, filemode = 'w', level=logging.DEBUG,)

class SSHDev:
  def __init__(self, hostname = '192.168.2.110', mykey = '~/.ssh/id_rsa', username = 'root', cmd = '', proc = '', k_proc = '', password = ''):
    self.hostname = hostname
    self.mykey = mykey
    self.username = username
    self.proc = proc
    self.k_proc = k_proc
    self.password = password
    self.cmd = cmd
  
  def send_cmd(self):
    logging.debug('Connecting to ' + self.hostname + ' user: ' + self.username + ' key-file: ' + self.mykey + ' and executing ' + self.cmd)
    try:
      s = ssh.Connection(self.hostname, self.username, private_key = self.mykey)
    except Exception, e:
      logging.debug('Exception from connecting: \n' + str(e))
      return "Connection failed! " + str(e)
    #s.put()
    #s.get('goodbye.txt')  
    rep = s.execute(self.cmd)
    logging.debug('Output from sending command: ' + str(rep))
    ret = '\n'.join(rep)
    #s.put('/home/serg/embedded.txt', '/root/embe.txt')
    #s.get('getall.sh', '/home/serg/dogogo.sh')
    s.close()
    logging.debug('Returning: ' + str(ret))
    return ret
  
  def find_pid(self):
    try:
      s = ssh.Connection(self.hostname, self.username, private_key = self.mykey)
    except Exception, e:
      logging.debug('Exception from connecting: \n' + str(e))
      return "Connection failed! " + str(e)
    
    res = s.execute('ps aux | grep ' + self.proc + ' | grep -v grep')
    logging.debug('From grep got ' + str('\n'.join(res)))
    try:
      if res[0].split()[0] == 'root':
        pid = res[0].split()[1]
        logging.debug('PID of process ' + self.proc + ' is ' + pid)
    except Exception, e:
      logging.debug('Exception from pid search: \n' + str(e))
      return "Mea culpa! PID not found"
    s.close()
    return pid
  
  def kill_proc(self):
    try:
      s = ssh.Connection(self.hostname, self.username, private_key = self.mykey)
    except Exception, e:
      logging.debug('Exception from connecting: \n' + str(e))
      return "Mea culpa! Connection failed! " + str(e)
    try:
      logging.debug('Search for the process\' PID: \n' + self.k_proc)
      find_pid_obj = SSHDev(proc = self.k_proc)
      pid = find_pid_obj.find_pid()
    except Exception, e:
      logging.debug('Exception from pid search: \n' + str(e))
      return 'Exception from pid search: \n' + str(e)
    logging.debug('Killig process ' + self.k_proc + ' with PID=' + pid)
    if 'Mea culpa' not in pid: res = s.execute('kill -9 ' + pid)
    else: return 'Mea culpa! Killing failed. See log in '+LOG_FILENAME
    logging.debug('Output was ' + str(res))
    res = '\n'.join(res)
    s.close()
    return res

def main(*args):
  sshc = SSHDev(k_proc = 'sleep')
  print sshc.kill_proc()
  #print SSHDev.send_cmd(cmd = 'ps aux')
  #print SSHDev.find_pid(proc = 'java')
  #print SSHDev.kill_proc(hostname = '192.168.2.110', k_proc = 'sleep')
        
if __name__ == '__main__':
  main(sys.argv)

