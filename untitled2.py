# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 11:08:04 2015

@author: 3820104
"""
import colorsys
import numpy as np
import matplotlib.pyplot as plt

def simplepseudocolor(val, minval, maxval):
    # convert val in range minval...maxval to range 0..1
    f = float(val-minval) / (maxval-minval)
    # linearly interpolate that value between the colors red and green
    r, g, b = 1-f, f, 0.
    return r, g, b

def test_simplepseudocolor():
    #fig = plt.figure()
    #ax1 = fig.add_subplot(111)
    steps = 1
    print 'val       R      G      B'
    for val in xrange(0, 100+steps, steps):
        r,g,b = simplepseudocolor(val, 0, 100)
        #print '%3d -> (%.3f, %.3f, %.3f)' % ((val,) + simplepseudocolor(val, 0, 100))
        plt.plot([val/10., val/10.],[0, 1],color=[r,g,b])
    plt.show()
        
def pseudocolor(val, minval, maxval):
    # convert val in range minval..maxval to the range 0..120 degrees which
    # correspond to the colors red..green in the HSV colorspace
    h = (float(val-minval) / (maxval-minval)) * 120
    # convert hsv color (h,1,1) to its rgb equivalent
    # note: the hsv_to_rgb() function expects h to be in the range 0..1 not 0..360
    r, g, b = colorsys.hsv_to_rgb(h/360, 1., 1.)
    return r, g, b

def test_pseudocolor():
    steps = 10
    print 'val       R      G      B'
    for val in xrange(0, 100+steps, steps):
        print '%3d -> (%.3f, %.3f, %.3f)' % ((val,) + pseudocolor(val, 0, 100))


#http://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

def test_rgb():    
    for i in xrange(10,30,2):
        r,g,b = rgb(10,30,i)
        print '{:.3f} -> ({:3d},{:3d},{:3d},)'.format(i, r, g, b)
    
test_simplepseudocolor()

#http://matplotlib.org/users/artists.html
def simpleplot():
    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
    ax1 = fig.add_subplot(211)
    ax1.set_ylabel('volts')
    ax1.set_title('a sine wave')
    
    t = np.arange(0.0, 1.0, 0.01)
    s = np.sin(2*np.pi*t)
    line, = ax1.plot(t, s, color='blue', lw=2)
