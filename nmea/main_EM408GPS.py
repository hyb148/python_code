import re

#http://doschman.blogspot.com/2013/01/parsing-nmea-sentences-from-gps-with.html

def main():

    device = EM408GPS("/dev/ttyAMA0", 4800)

    newdata = ""
    line = ""

    while device.isOpen():
         # If we have new data from the data CRLF split, then 
         # it's the start + data of our next NMEA sentence.  
         # Have it be the start of the new line
         if newdata: 
             line = newdata
             newdata = ""
         
         # Read from the input buffer and append it to our line 
         # being constructed
         line = line + device.readBuffer()
            
         # Look for  \x0d\x0a or \r\n at the end of the line (CRLF) 
         # after each input buffer read so we can find the end of our 
         # line being constructed
         if re.search("\r\n", line):
             
             # Since we found a CRLF, split it out
             data, newdata = line.split("\r\n")

             print "----" + str(datetime.datetime.now()) + "----"
             print data
             print
                    
             # Reset our line constructer variable
             line = ""