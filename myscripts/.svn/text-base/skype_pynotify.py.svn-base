# 2008-2009, Sergey Korablin skorablin@gmail.com

#!/usr/bin/env python
 
import sys
import Skype4Py
import pygtk
pygtk.require('2.0')
import pynotify
import threading

mystatus =0;
texts = ''

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

class Got_User(threading.Thread):
	def __init__(self, cmd_f):
		self.Cmd = cmd_f
	
	def run(self):
		try:
			## Switch to low-level, API doesn't understand user's upper case
				cmd_low = self.Cmd.lower()
				#print "Input was %s, asking about %s"%(Cmd, cmd_low)
				#user = skype.User(cmd_low);
				found = 0
				for friend in skype.Friends:
					if friend.Handle.lower().find(cmd_low) != -1: user = skype.User(friend.Handle); found = 1
					elif friend.DisplayName.lower().find(cmd_low) != -1: user = skype.User(friend.Handle); found = 1
					elif friend.FullName.lower().find(cmd_low) != -1: user = skype.User(friend.Handle); found = 1
					
				
				if found:
					print "User " + user.FullName + " is " + user.OnlineStatus + ", from  " + user.City;
					username = user.Handle
				else:	print "User %s is not among your friends, doesn't know about him!"%self.Cmd; 
				"""
				try:
					print dir(user)
					
					
				except Exception, e:
					print "Failed because: ", e
				
				try: print "Debug", Cmd, cmd_low, user, user.Handle, user.DisplayName, user.FullName, user.OnlineStatus
				except: pass
				"""
				try:
					print username
					uchat = skype.CreateChatWith(username)
					uchat.SendMessage('privet')
					
				except Exception, e:
					print "WRONG!\n%s"%str(e)
				
		except Exception, e:
			print "Online status of user " + Cmd + " is unknown!\n%s"%str(e)
			


notifies = []

# Creating instance of Skype object, assigning handler functions and attaching to Skype.
skype = Skype4Py.Skype(Events=MySkypeEvents());
#skype = Skype4Py.Skype()
skypeu = Skype4Py.Skype()


if not skype.Client.IsRunning:
	print "Skype not running";
	sys.exit(1)


if not pynotify.init("Basics"):
		sys.exit(1)
n = pynotify.Notification("Test message", "skype");
n.set_timeout(10000);
n.show();

print('******************************************************************************');
print 'Connecting to Skype..'
try: skype.Attach()
except Exception, e: print "FAILED connect to Skype!\n%s"%str(e)

# Looping until user types 'exit'
Cmd = '';
while not Cmd == 'exit':
	Cmd = raw_input('');
	if Cmd == 'status':
		print "status: ", mystatus; 
	else:
		Got_User(Cmd).run()
# 	user._Skype._DoCommand('GET USER %s AVATAR 1 /tmp/useravatar',user.Handle);



