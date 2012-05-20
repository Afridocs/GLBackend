from zope.interface import Interface, Attribute
from twisted.internet import defer
from twisted.internet import reactor


import itertools

def spawnDeferredTasks(taskList):
    """
    Run several Tasks concurrently.
    """
    def callback(result, task):
        print "I got callback spawn %s" % result
        #print task.receiver
        if len(taskList) > 0:
            task = taskList.pop(0)
            print len(taskList)
            task.startTask()

    def errback(reason, task):
        #print "I got errback spawn %s" % reason
        #print task
        # XXX Write to log that the first work failed
        # XXX add maximum amount of retries
        # taskList.append(task)
        try:
            task = taskList.pop(0)
            task.startTask()
        except:
            pass

    deferredList = []
    for task in taskList:
        deferred = task.deferred
        deferred.addCallback(callback, task).addErrback(errback, task)

        deferredList.append(deferred)

    for i in range(min(10, len(taskList))):
        try:
            task = taskList.pop(0)
            #print "in range shit"
            #print task.receiver
            #print len(taskList)
            task.startTask()
        except:
            print i

    return deferredList

class DummyMethod:
    def __init__(self, type):
        self.type = type
        self.deferred = defer.Deferred()

    def deliver(self, receiver):
        print "Doing delivery via %s" % self.type
        print "To: %s" % receiver

    def notify(self, receiver):
        print "Doing notification via %s" % self.type
        print "To: %s" % receiver

class Task:
    """
    Object responsible for handling the creation of delivery and notification
    task to receivers.
<<<<<<< HEAD
    """
    receiver = None
    type = None
    tip = None

    def __init__(self, type, receiver, tip):
        self.type = type
        self.receiver = receiver
        self.notify_method = self._get_notification_method()
        self.delivery_method = self._get_delivery_method()
        self.tip = tip
        self.deferred = defer.Deferred()
        #self.deferred.addCallbacks(self.callback, self.errback)

    def _get_delivery_method(self):
        return DummyMethod(self.type)

    def _get_notification_method(self):
        return DummyMethod(self.type)

    def spam_check(self):
        pass

    def doneTask(self):
        self.delivery_method.deliver(self.receiver)
        self.notify_method.notify(self.receiver)
        self.deferred.callback(str(self.receiver))

    def startTask(self):
        print "Starting task %s" % (self.receiver)
        reactor.callLater(1, self.doneTask)
        return self.deferred

def success(aa):
    print "DOne!"

def failed(bbb):
    print "Failed"

taskList = [Task('email', 'art'+str(x)+'@fuffa.org', {'a':1, 'b':2}) for x in range(0, 20)]

deferredList = spawnDeferredTasks(taskList)
#for deferred, task in zip(deferredList, taskList):
#    deferred.addCallback(success).addErrback(failed)
#deferred = defer.DeferredList(deferredList)
#deferred.addCallback(success)

reactor.run()
