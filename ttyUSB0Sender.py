#!/usr/bin/env python

import serial
import time
 
class Sender:
    def __init__(self, recipient="", message=""):
        self.recipient = recipient
        self.content = message
 
    def setRecipient(self, number):
        self.recipient = number
 
    def setContent(self, message):
        self.content = message
 
    def connectPhone(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
        time.sleep(1)
 
    def sendMessage(self):
        self.ser.write('AT\r\n'.encode())
        time.sleep(1)
        self.ser.write('AT+CMGF=1\r\n'.encode())
        time.sleep(1)
        self.ser.write('''AT+CMGS="'''.encode() + self.recipient.encode() + '''"\r\n'''.encode())
        time.sleep(1)
        self.ser.write(self.content.encode() + '\r\n'.encode())
        time.sleep(1)
        msg = self.ser.write(chr(26).encode())
        return msg
 
    def disconnectPhone(self):
        self.ser.close()
