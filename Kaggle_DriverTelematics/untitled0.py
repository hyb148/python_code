# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:15:01 2015

@author: 3820104
"""
#import csv
import numpy as np
import matplotlib.pyplot as plt
import math as math
import os
"""
with open('./drivers/1/1.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print row
"""

def showStats(name,data):
    std = np.std(data)
    s2 = 0
    s = 0
    for e in data:
        s += e
        s2 += e * e
    s = s/len(data)
    s2 = s2/len(data) - s**2
    #print name, ': mean =',s,'variance =',s2,'std dev = ',std
    return (s, s2, std)    

def getMetrics(data):
    # x, y
    # data['col1_name'], data['col2_name']
    datalen = len(data['x'])
    x = data['x']
    y = data['y']
    # dx
    dx = np.empty([datalen,1])
    dx[0] = 0
    # yaw
    yaw = np.empty([datalen,1])
    yaw[0] = 0
    # acc
    acc = np.empty([datalen,1])
    acc[0] = 0
    acc[1] = 0
    # dyaw
    dyaw = np.empty([datalen,1])
    dyaw[0] = 0
    dyaw[1] = 0
    # jerk
    jerk = np.empty([datalen,1])
    jerk[0] = 0
    for i in range(1,datalen):
        a = (x[i]-x[i-1])
        b = (y[i]-y[i-1])
        dx[i] = math.sqrt(a**2 + b**2)
        yaw[i] = math.atan2(b,a)
        acc[i] = dx[i]-dx[i-1]
        dyaw[i] = yaw[i]-yaw[i-1]
        jerk[i] = acc[i]-acc[i-1]
    try :
        # eliminate low speed data
        index = np.where(dx>0)[0]
        dx = dx[index]
        yaw = yaw[index]
        acc = abs(acc[index])
        dyaw = abs(dyaw[index])
        jerk = abs(jerk[index])
        #
        yaw = yaw *180/math.pi
        dyaw = dyaw*180/math.pi
        # eliminate low acceleration data
        index = np.where(acc > .1)[0]
        dx = dx[index]
        yaw = yaw[index]
        acc = acc[index]
        dyaw = dyaw[index]
        jerk = jerk[index]
        #
        accdx = acc/dx
        dyawXacc = dyaw*acc
        dyawDdx = dyaw/dx
        #
        if(False):
            plt.figure()
            plt.subplot(251)
            plt.plot(x,y)
            plt.title('x,y')
            plt.subplot(252)
            plt.plot(dx)
            plt.title('dx')
            plt.subplot(253)
            plt.plot(abs(acc))
            plt.title('abs(acc)')
            plt.subplot(254)
            plt.plot(accdx)
            plt.title('abs(acc)/dx')
            plt.subplot(255)
            plt.plot(jerk)
            plt.title('jerk')
            plt.subplot(256)
            plt.plot(abs(yaw))
            plt.xlabel('yaw')
            plt.subplot(257)
            plt.plot(abs(dyaw))
            plt.xlabel('abs(dyaw)')
            plt.subplot(258)
            
            
            plt.plot(dyawXacc)
            plt.xlabel('abs(dyaw)*abs(acc)')
            #plt.xlim([-5,5])
            plt.subplot(248)
            plt.plot(dyawDdx)
            plt.xlabel('abs(dyaw)/dx')
            #plt.ylim([-10, 20])
            plt.show()
        
        """
        dx = dx[index]
        yaw = yaw[index]
        acc = acc[index]
        dyaw = dyaw[index]
        jerk = jerk[index]
        #
        accdx = acc/dx
        dyawXacc = dyaw*acc
        dyawDdx = dyaw/dx
        """
        a = ['dx','yaw','acc','dyaw','jerk','accdx','dyawXacc','dyawDdx']
        b = [dx,yaw,acc,dyaw,jerk,accdx,dyawXacc,dyawDdx]
        metrics = []
        for i, j in zip(a,b) :
            s, s2, std = showStats(i,j)
            metrics.extend(s)
    except :
        metrics = [0]*len(b)
    return metrics

path = './drivers/'
dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
for i in range(len(dirs)):
    dirpath = path+dirs[i]+'/' 
    outfile = path+'_'+dirs[i]+'_results.txt'
    if(os.path.exists(outfile)==False):
        if(os.path.exists(dirpath) and os.path.isdir(dirpath)):
            onlyfiles = [os.path.join(dirpath,fn) for fn in next(os.walk(dirpath))[2]] #[ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
            metrics = np.empty((len(onlyfiles),8), float)
            index = 0
            for i in onlyfiles:
                if(i.find('.csv')>0): #
                    print 'processing ',i
                    data = np.genfromtxt(i, dtype=float, delimiter=',', names=True)
                    run_metrics = getMetrics(data)
                    metrics[index] = run_metrics
                    index += 1
            print index, 'files processed'
            np.savetxt(outfile,metrics,delimiter=',')