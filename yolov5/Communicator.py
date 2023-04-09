import serial
import ujson
from pyudev import Context

class Communicator:
    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.serial = None
        self.initialized = self.reset_USB_port()
    
    def reset_USB_port(self):
        # Find devices corresponding to /dev/ttyUSB*
        context = Context()
        device_list = list(context.list_devices(subsystem='tty', ID_BUS='usb'))
                
        # Check if there is a USB device at all. If so, pick one and set it as the port
        if len(device_list) == 0:
            print("No USB device found. Can't communicate with LoRa")
            self.initialized = False
            return False
        
        # If there is more than one USB device, pick the first one
        elif len(device_list) > 1:
            print("More than one USB device found. Picking the first one and whatever happens happens!")
            self.port = device_list[0].device_node
        
        # If there is only one USB device, pick it
        else:
            self.port = device_list[0].device_node
        
        self.initialized = True
        self.serial = serial.Serial(self.port, baudrate=self.baudrate)
        return True
    
    def send(self, message):
        if self.initialized:
            message = message + "\n"  # Add signal \n to signal the end of the message
            self.serial.write(bytes(message,'utf-8'))
            print("Sent message: " + message)
        elif self.reset_USB_port():
            # Reset port and retry sending
            self.serial.write(bytes(message,'utf-8'))
            print("Sent message: " + message)
        else:
            print("Can't send message. Not initialized")
    
    def receive(self):
        if self.initialized:
            return self.serial.readline().decode()
        else:
            print("Can't receive message. Not initialized")
            return None
    
    def close(self):
        if self.initialized:
            self.serial.close()
            print("Closed serial connection")
        else:
            print("Can't close serial connection. Not initialized")
