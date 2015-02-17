import serial 

class EM408GPS:
    
    def __init__(self, serialport, baudratespeed):

        self.gpsdevice = serial.Serial(port=serialport, baudrate=baudratespeed, timeout=5)
        
        self.init()

    def init(self):
        
        if self.isOpen():
            return True
        
        return False

    def open(self):
        self.gpsdevice.open()
        
    def isOpen(self):
        return self.gpsdevice.isOpen()
def readBuffer(self):

        try:
            data = self.gpsdevice.read(1)
            
            n = self.gpsdevice.inWaiting()
            
            if n:
                data = data + self.gpsdevice.read(n)
        
            return data

        except Exception, e:
            print "Big time read error, what happened: ", e
            sys.exit(1)

