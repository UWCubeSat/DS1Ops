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
        self.stop = False
        
    def run(self):
        inpt = 'start' 
        while len(inpt) > 0 and not self.stop:
            try:
                inpt = self.skt.recv(1024)
                
            except:
                pass
            
            now = datetime.utcnow()
            passes = [[now, now, now]]
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
                #send location packet
                try:
                    self.skt.send(packet)
                except:
                    print("could not send packet")
                    
                time.sleep(1)
                now = datetime.utcnow()
                
                next_passes = orb.get_next_passes(now, 24, -122.3032, 47.655548, 150 , tol=0.001, horizon=0)
               
                if len(next_passes) > 0:
                    #check if both rise and fall are in the future or both in the past
                    if ((passes[0][0] - now).total_seconds())*((passes[0][1] - now).total_seconds()) >= 0:
                        passes = next_passes
               
                
                rise = (passes[0][0] - now).total_seconds()
                
                fall = (passes[0][1] - now).total_seconds()
                packet = "\x02".encode()
                packet += bytearray(struct.pack("i",int(rise)))
                packet += bytearray(struct.pack("i",int(fall)))
                
                
                #send time packet
                try:
                    self.skt.send(packet)
                except:
                    print("could not send packet")
            except:
                print("could not read tle file at "+ self.tle_location)
        print("connection to "+ addr[0] + " closed")
        self.skt.close()


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("", 5555)) 
s.listen(5)
s.settimeout(3)

num_threads = 0
running = True
services = []

while running:
    try:
        con, addr = s.accept()
        print("connected to "+ addr[0])    
        con.settimeout(1)
        p_serv = Propigation_Service("AO-85", num_threads, "tle.txt", con , 600000, addr)            
        p_serv.start()
        services.append(p_serv) 
        num_threads += 1

    except Exception as ex:
        if ex == 'KeyboardInterupt':
            running = False
            for s in services:
                s.stop = True
s.close()
