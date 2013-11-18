#!/usr/bin/env python

import Skype4Py
import threading


class MySkypeEvents:
  def UserMood(self, User, MoodText):
    print User.FullName + " " + MoodText;

  def UserStatus(self,status):
    print 'User status has changed to ' + status

  def OnlineStatus(self, User, Status):
    print 'User ' + User.FullName + " is " + Status;
    n = pynotify.Notification(User.FullName, "user is " + Status, "skype");
    n.set_timeout(10000);
    n.show();

# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
  def AttachmentStatus(self, Status):
    mystatus = Status;
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(Status) + " (",Status , ")";
    if Status == Skype4Py.apiAttachAvailable:
      skype.Attach();
    
    if Status == Skype4Py.apiAttachSuccess:
      print('******************************************************************************');


# Fired on chat message status change. 
# Statuses can be: 'UNKNOWN' 'SENDING' 'SENT' 'RECEIVED' 'READ'    

  def MessageStatus(self,Message, Status):
    print "Message status: " + Status;
    if Status == 'RECEIVED':
      global texts
      print "Debug!!! ", Message.Body
      if len(texts) < 100:
        texts += Message.Body + '\n'
        try:
          n = notifies.pop()
          n.close()
        except:
          pass
      n = pynotify.Notification(Message.FromDisplayName, texts,"skype")
      n.set_timeout(0)
      #n.set_timeout(pynotify.EXPIRES_NEVER)
      if not n.show():
        print "Failed to send notification"
      else:
        notifies.append(n)
    
    if Status == 'SENT':
      print('Myself: ' + Message.Body + ': ' + Message.Type);
    if Status == 'READ':
      try:
        n = notifies.pop()
        n.close()
        texts = ''
      except:
        pass