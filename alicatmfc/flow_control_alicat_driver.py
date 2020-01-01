import serial
import serial.tools.list_ports
from serial import SerialException
import time

def tryPort(port):
    """Checks the connection to a serial port. Returns True or error string."""
    result = False
    try:
        p = serial.Serial(port)
        result = True
        p.close()
    except SerialException:
        return ("COM Failure!", "Could not connect to " + port)
        result = False
    return result

class flow_controller:
    def __init__(self, port, unit_ID):
        self.port = port
        self.unit_ID = unit_ID
    
    def ping(self):
        '''Check communication with flow controller. Returns True or error string '''
        result = tryPort(self.port)
        if result != True:
            return result
        # set flow to zero
        self.setMFC(0) 
        result = self.checkFlowStability()
        if result == True:
            return True
        if result == False:
            i = 10
            while( self.checkFlowStability() == False ):
                i = i-1
                if i == 0:
                    return "Error, MFC initialized, but flow not stable."
                    break
            return True
        else:
            return result
        
    def setMFC(self, setpoint):
        """Set the MFC to a given flow point and make sure the MFC responds. Returns Error string or rx_data from MFC."""
        tryPort(self.port)
        com = serial.Serial(self.port)
        com.timeout = .1
        com.baudrate = 19200
        #command = unit_ID + str(setpoint/flowRange*64000) + "\r"
        command = self.unit_ID + "S" + str(setpoint) + '\r'
        com.write(command.encode())
        rx_data = com.read_until('\r').decode('ascii').rstrip('\r')
        com.close()
        if len(rx_data)==0:
            return "Error, MFC " + self.unit_ID + " on " + self.port + " did not respond"
        if rx_data[0]!=self.unit_ID:
            return "Error, MFC " + self.unit_ID + "on" + self.port + "did not respond"
        return rx_data
    
    def checkFlowStability(self):
        """Checks if the MFC has stabilized. Returns True or False or Error string."""
        tryPort(self.port)
        com = serial.Serial(self.port)
        com.timeout = .1
        com.baudrate = 19200
        command = self.unit_ID + '\r'
        com.write(command.encode())
        rx_data = com.read_until('\r').decode('ascii').rstrip('\r')
        com.close()
        if len(rx_data)==0:
            return "Error, MFC " + self.unit_ID + " on " + self.port + " did not respond"
        if rx_data[0]!=self.unit_ID:
            return "Error, MFC " + self.unit_ID + "on" + self.port + "did not respond"
        rx_data_list = rx_data.split(' ')
        if ( abs(float(rx_data_list[4])-float(rx_data_list[5])) < 0.2 ):
            return True
        else:
            return False
			