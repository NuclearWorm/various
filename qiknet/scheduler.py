import heapq, asyncore, time

class MyScheduler(object):
  def __init__(self):
    self.taskqueue = []
    pass
  def addTaskImmediately(self, func, args):
    heapq.heappush(self.taskqueue, (0, func, args))
  def addTaskAt(self, func, args, then):
    heapq.heappush(self.taskqueue, (then, func, args))
  def addTaskIn(self, func, args, delay):
    then = time.time()+delay
    heapq.heappush(self.taskqueue, (then, func, args))
  def run(self, use_poll=False, map=None):
    if map is None:
      map = asyncore.socket_map
  
    if use_poll and hasattr(asyncore.select, 'poll'):
      poll_fun = asyncore.poll2
    else:
      poll_fun = asyncore.poll
  
    while map or self.taskqueue:
#      print '#'
      if len(self.taskqueue) > 0:
        (then, func, args) = self.taskqueue[0]
        timeout = then - time.time()
#        print 'Timeout %d'%timeout        
        if timeout <= 0:
          (then, func, args) = heapq.heappop(self.taskqueue)
          func(self, args)
          timeout = 0
#          continue
      else:
#        print '!!! No task in queue'
        timeout = 30
#      print 'Calling poll with timeout:%f'%timeout
      poll_fun(timeout, map)

