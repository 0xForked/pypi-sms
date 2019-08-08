#!/usr/bin/env python
from ttyUSB0Sender import Sender

class Message:
    def __init__(self, result):
        self.id = result[0]
        self.number = result[1]
        self.provider = result[2]
        self.message = result[3]
        self.status = result[4]
        
    def send(self):
        sender = Sender(self.number, self.message)
        sender.connectPhone()
        callback = sender.sendMessage()
        sender.disconnectPhone()
        return callback, self.id
