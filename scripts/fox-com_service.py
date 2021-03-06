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
      self.time_since_last_command = 0
      self.time_since_last_connect = 0
      self.error_log = []
      self.close = threading.Event()
    def run(self):
        while not self.close.is_set():
            try:
                con, addr = self.skt.accept()
                self.time_since_last_connnect = 0
                con.settimeout(.5)
                if not self.mute.is_set():
                    print("COSMOS Connected")
                inpt = "start"
                while len(inpt) != 0 and not self.close.is_set():
                    try:
                        inpt = con.recv(1024) 
                        if len(inpt) > 0:
                            if not self.mute.is_set():
                                print( "Recieved" +str(inpt))
                            self.time_since_last_command = 0
                            self.command_queue.put(inpt)
                    except Exception as e:
                        if str(e) != 'timed out':
                            self.error_log.append(str(e))
                        self.time_since_last_command += .5
                con.shutdown(socket.SHUT_RDWR)
                con.close()
                if not self.mute.is_set():
                    print("COSMOS Disconnected")
            except:
                self.time_since_last_connect += 3
                if not self.mute.is_set():
                    print("Not connected to COSMOS")
        self.skt.shutdown(socket.SHUT_RDWR)
        self.skt.close()
        print('cosmos listener closed')
    def get_error_log(self):
        return self.error_log
    def get_last_command_time(self):
        return self.time_since_last_command

    def get_last_connect_time(self):
        return self.time_since_last_connect

class Fox_com_Sender(threading.Thread):
    def __init__(self, threadID, name, addr, port, command_queue):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.mute = threading.Event()
      self.addr = addr
      self.port = port
      self.command_queue = command_queue
      self.close = threading.Event()
    def run(self):
        
        while not self.close.is_set():
            time.sleep(4.5)
            if not self.command_queue.empty(): 
               try:
                  skt = socket.socket()
                  skt.settimeout(3)
                  skt.connect((self.addr, self.port))
                  inpt = "start"
                  try:
                     inpt = skt.recv(1024).decode("utf-8") 
                  except:
                     pass
                  cmd = self.command_queue.get()
                  skt.send(cmd)
                  if not self.mute.is_set():
                       print("Sent "+ str(cmd) )
                  skt.close()
               except:
                  skt.close()
                  if not self.mute.is_set():
                       print("Not connected to fox com")
        print('fox com sender closed')


s_cosmos= socket.socket()
host = ""
s_cosmos.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_cosmos.bind((host, 4444))
s_cosmos.listen(5)

thread_num = 0
command_queue = queue.Queue()
t_csms = COSMOS_Listener(thread_num, "csms", s_cosmos, command_queue)
   
t_fx_cm = Fox_com_Sender(thread_num, "fox", "192.168.1.159", 8897, command_queue)
thread_num += 1
t_csms.start()
t_fx_cm.start()

running = True

while running:
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
    elif cmd == 'clear':
        command_queue.queue.clear()
    elif cmd == 'quit':
        t_csms.close.set()
        t_fx_cm.close.set()
        running = False
    elif cmd == 'get-last-command-time':
        print(t_csms.get_last_command_time())
    elif cmd == 'get-last-connect-time':
        print(t_csms.get_last_connect_time())
    elif cmd == 'get-error-log':
        for e in t_csms.get_error_log():
            print(e)
    elif cmd == 'help':
        print('mute: mutes print outs\n \
unmute: unmute print outs\n \
view-queue: print queued commands\n \
clear: clear command queue\n \
get-last-command-time: get the time since the last command was recieved\n \
get-last-connect-time: get time since last time cosmos was connected\n \
get-error-log: get the errors that have happend while reading commands\n \
quit: close the service')
    elif cmd == 'get-last-command-time': 
        print(t_csms.get_time_since_last_command())
    else:
        print('type help to get available commands')

