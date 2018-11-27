import socket
import threading
import queue
import time

class COSMOS_Listener(threading.Thread):
    def __init__(self, threadID, name, skt, command_queue):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.skt = skt
      self.command_queue = command_queue
      self.skt.settimeout(3)
    def run(self):
        while True:
            try:
                con, addr = self.skt.accept()
                print("COSMOS Connected")
                inpt = con.recv(1024) 
                while len(inpt) != 0:
                    inpt = con.recv(1024) 
                    if len(inpt) > 0:
                        print( "Recieved" +str(inpt))
                        self.command_queue.put(inpt)
                print("COSMOS Disconnected")
                con.close()
            except:
                print("Not connected to COSMOS")

class Fox_com_Listener(threading.Thread):
    def __init__(self, threadID, name, skt, command_queue):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.skt = skt
      self.command_queue = command_queue
      self.skt.settimeout(3)
    def run(self):
        while True:
            try:
                con, addr = self.skt.accept()
                print("Fox Com Connected")
                con.settimeout(.01)
                inpt = "start"
                while len(inpt) != 0 :
                   
                    try:
                        inpt = con.recv(1024).decode("utf-8")
                        
                    except:
                        pass
                    time.sleep(3)
                    if  not self.command_queue.empty() :
                        cmd = self.command_queue.get()
                        print("Sent "+ str(cmd) )
                        con.send(cmd)
                    
                con.close()
                print("fox Com Disconnected")
            except:
                print("Not connected to fox com")


s_cosmos= socket.socket()
s_fox_com = socket.socket()
host = ""

s_cosmos.bind((host, 5555))
s_fox_com.bind((host, 4444))
s_cosmos.listen(5)
s_fox_com.listen(5)
thread_num = 0
command_queue = queue.Queue()
t_csms = COSMOS_Listener(thread_num, "csms", s_cosmos, command_queue)
   
t_fx_cm = Fox_com_Listener(thread_num, "fox", s_fox_com, command_queue)
thread_num += 1
t_csms.daemon = True
t_fx_cm.daemon = True
t_csms.start()
t_fx_cm.start()

while True:
    time.sleep(1)