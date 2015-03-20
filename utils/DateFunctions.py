# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 12:27:58 2015

@author: 3820104
"""
import datetime


def weekDay(year, month, day):
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    week   = ['Sunday', 
              'Monday', 
              'Tuesday', 
              'Wednesday', 
              'Thursday',  
              'Friday', 
              'Saturday']
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    # dayOfWeek for 1700/1/1 = 5, Friday
    dayOfWeek  = 5
    # partial sum of days betweem current date and 1700/1/1
    dayOfWeek += (aux + afterFeb) * 365                  
    # leap year correction    
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400     
    # sum monthly and day offsets
    dayOfWeek += offset[month - 1] + (day - 1)               
    dayOfWeek %= 7
    return dayOfWeek, week[dayOfWeek]


def DayOfWeek(year,month,day):
    DayL = ['Mon','Tues','Wednes','Thurs','Fri','Satur','Sun']
    date = DayL[datetime.date(year,month,day).weekday()] + 'day'
    #Set day, month, year to your value
    #Now, date is set as an actual day, not a number from 0 to 6.

    #print(date)
    return date
    
print weekDay(2000,12,12)
print weekDay(2014,12,30)

print DayOfWeek(2000,12,12)