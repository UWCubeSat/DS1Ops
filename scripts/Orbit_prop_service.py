# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:37:14 2019

@author: Langley
"""

from pyorbital.orbital import Orbital
from datetime import datetime
import socket
import threading
import urllib
import struct
import time


class Propigation_Service(threading.Thread):
    def __init__(self, name, threadID, tle_location, skt, update_period, addr):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID
        self.tle_location=tle_location
        self.skt = skt
        self.update_period = update_period
        self.last_update = datetime(1970,1,1)
        
    def run(self):
        inpt = "foo"
        
        while len(inpt) > 0:
            try:
                inpt = self.skt.recv(1024)
                
            except:
                pass
            
            now = datetime.utcnow()
            
            if (now-self.last_update).total_seconds() > self.update_period:
                try:
                    print("updating tle file")
                    data = urllib.request.urlopen("https://www.amsat.org/tle/current/nasa.all")
                    file = open("tle.txt",'w')
                    for line in data:
                        file.write(line.decode("utf-8"))
                    file.close()
                    self.last_update = now
                    print("tle file updated")
                except:
                    print("could not update tle file")
            
            try:
                now = datetime.utcnow()
                orb = Orbital(self.name, tle_file=self.tle_location)
                loc=orb.get_lonlatalt(datetime.utcnow())
                
                
                packet = "\x01".encode()
                
                packet += bytearray(struct.pack("f",loc[0]))
                packet += bytearray(struct.pack("f",loc[1]))
                packet += bytearray(struct.pack("f",loc[2]))
                try:
                    self.skt.send(packet)
                except:
                    print("could not send packet")
                    
                time.sleep(1)
                now = datetime.utcnow()
                passes = orb.get_next_passes(now, 2, -122.308932, 47.654030999999996, 50, tol=0.001, horizon=0)
                rise = (passes[0][0] - now).total_seconds()
                fall = (passes[0][1] - now).total_seconds()
                packet = "\x02".encode()
                packet += bytearray(struct.pack("i",int(rise)))
                packet += bytearray(struct.pack("i",int(fall)))
                
                time.sleep(1)
                try:
                    self.skt.send(packet)
                except:
                    print("could not send packet")
            except:
                print("could not read tle file at "+ self.tle_location)
        print("connection to "+ addr[0] + " closed")
        self.skt.close()

#orb = Orbital("AO-85", tle_file="tle.txt")

#print(orb.get_lonlatalt(datetime.utcnow()))

while True:
    s = socket.socket()
    s.bind(("", 5555))
    s.listen(5)
    s.settimeout(3)
    num_threads = 0
    try:
        con, addr = s.accept()
        print("connected to "+ addr[0])
        
        con.settimeout(1)
        p_serv = Propigation_Service("AO-85", num_threads, "tle.txt", con , 600000, addr)
        
        p_serv.start()
        
        num_threads +=1
    except:
        pass