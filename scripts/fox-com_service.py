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
      self.mute = threading.Event()
      self.skt.settimeout(3)
    def run(self):
        while True:
            try:
                con, addr = self.skt.accept()
                if not self.mute.is_set():
                    print("COSMOS Connected")
                inpt = "start"
                while len(inpt) != 0:
                    try:
                        inpt = con.recv(1024) 
                        if len(inpt) > 0:
                            if not self.mute.is_set():
                                print( "Recieved" +str(inpt))
                            self.command_queue.put(inpt)
                    except:
                        pass
                if not self.mute.is_set():
                    print("COSMOS Disconnected")
                con.close()
            except:
                if not self.mute.is_set():
                    print("Not connected to COSMOS")

class Fox_com_Sender(threading.Thread):
    def __init__(self, threadID, name, addr, port, command_queue):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.mute = threading.Event()
      self.addr = addr
      self.port = port
      self.command_queue = command_queue
      
    def run(self):
        
        while True:
            
            try:
               skt = socket.socket()
               skt.settimeout(3)
               skt.connect((self.addr, self.port))
               if not self.mute.is_set():
                   print("Fox Com Connected")
                
               inpt = "start"
               while len(inpt) != 0 :   
                   try:
                       inpt = skt.recv(1024).decode("utf-8")    
                   except:
                       pass
                   time.sleep(4.5)
                   if  not self.command_queue.empty() :
                       cmd = self.command_queue.get()
                       if not self.mute.is_set():
                           print("Sent "+ str(cmd) )
                       skt.send(cmd)
                    
               skt.close()
               print("fox Com Disconnected")
            except:
                skt.close()
                if not self.mute.is_set():
                    print("Not connected to fox com")


s_cosmos= socket.socket()
host = ""
s_cosmos.bind((host, 5555))
s_cosmos.listen(5)
thread_num = 0
command_queue = queue.Queue()
t_csms = COSMOS_Listener(thread_num, "csms", s_cosmos, command_queue)
   
t_fx_cm = Fox_com_Sender(thread_num, "fox", "192.168.1.159", 8897, command_queue)
thread_num += 1
t_csms.start()
t_fx_cm.start()

while True:
    cmd=input(">>> ").strip()
    if cmd == "queue-length":
        print(str(command_queue.qsize()))
    elif cmd == "mute":
        t_csms.mute.set()
        t_fx_cm.mute.set()
    elif cmd == "unmute":
        t_csms.mute.clear()
        t_fx_cm.mute.clear()
    elif cmd == "view-queue":
        if command_queue.qsize() == 0:
            print("The queue is emtpy")
        for itm in list(command_queue.queue):
            print(str(itm))
