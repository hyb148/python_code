# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 13:18:33 2015

@author: 3820104
"""
import thread
import time

def runSerial(threadName, sleepTime):
    global loop_count
    global kill_flag
    while 1 < 2:
        time.sleep(sleepTime)
        print "%s" % (threadName)
        loop_count = loop_count -1
        if(loop_count < 1) :
            kill_flag = 1
            print threadName, " exiting."
            return

def runWatcher(threadName, sleepTime):
    global kill_flag
    while 1 < 2:
        time.sleep(sleepTime)
        print "%s" % (threadName)
        if(kill_flag > 0) :
            print threadName, " exiting."
            return


kill_flag = 0
loop_count = 10
try:
    thread.start_new_thread(runSerial,("runSerial",1))
    thread.start_new_thread(runWatcher,("runWatcher",2))
except Exception, e:
    print str(e)

