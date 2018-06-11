import serial.serialwin32
import threading
import os #os.environ["name"] = "value"
import sys
import win32com.shell.shell as shell
import ctypes

ports_list = [
        None,  #0
        "ADCS_BDOT",
        "MATLAB_BDOT",
        None,  #3
        None,  #4
        "PPT",
        "EPSDIST",
        "EPSGEN",
        "EPSBATT",
        "ADCS_ESTIM",
        "ADCS_MPC",
        "ADCS_SENSORPROC",
        "ADCS_MTQ",
        None,  #13
        None,  #14
        None   #15
    ]

def main():
    if isAdmin():
        for i in range(len(ports_list)):
            name = ports_list[i]
            if name:
                writeSSCOM(i, 256, "init")
            '''if name and not "FLATSAT_COMPORT_" + name in os.environ:
                print("adding environment variable for " + name)
                #os.system("call reg add \"HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment\"  /v FLATSAT_COMPORT_"+ name +" /d \"\"")  # calls the batch command
                writeSSCOM(i, 256) #this writes a default null value of 256'''
        print()
        timeout = 2  # seconds
        searchLen = 256  # attempts COMs 0 -> (searchLen - 1)
        threads = []
        for i in range(searchLen):
            t = threading.Thread(target=assignComPort, args=(i, timeout, 100))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print()
        os.system("pause")
    else:
        #run again as admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def writeSSCOM(ss_id, com_num,  output):
    if ports_list[ss_id]:
        var_name = "FLATSAT_COMPORT_" + ports_list[ss_id]
        #os.environ[var_name] = "COM" + str(com_num) #sets the current session's environment variables
        os.system("setx " + var_name + " COM" + str(com_num) + " -m > NUL") #calls the batch command
        if(output == "verbose"):
            print(var_name + " = COM" + str(com_num))
        elif(output == "init"):
            print(var_name + " assigned")
    else:
        print("id " + str(ss_id) + " not found")

def assignComPort(com_num, serial_timeout = 5, byte_timeout = 100, packet_timeout = 100):
    try:
        ser = serial.Serial('COM' + str(com_num), 9600, timeout=serial_timeout)
        packet_count = 0
        while packet_count < packet_timeout:
            output = receivePacketWithTimeout(ser, timeout=byte_timeout)
            if output:# and len(output) == 48:
                if len(output) == 48:
                    ss_id = output[1]
                    writeSSCOM(ss_id, com_num, "verbose")
                    return
                else:
                    packet_count += 1
            else:
                return
    except:
        return

def receivePacketWithTimeout(ser, timeout): #ser should be already open, timeout is the number of packets that aren't FC before the timeout gets hit; returns nothing if it times out
    timeout_count = 0
    while timeout_count < timeout:
        received = ser.read(1)
        if received == bytearray.fromhex('FC'): #start of a packet
            length = int(ser.read(1)[0] - 2) #length of the packet
            return ser.read(length)
        elif received: #byte received, but not the start of a packet
            timeout_count += 1
        else:
            return #timed out (seconds)

def sendPacket(ser, string):
    hex_data = bytes.fromhex(string)
    ser.write(hex_data)

def sendStartFire(ser, rate, timeout): #values must be < 10
    hex_str = 'FC060A02' + '0' + str(rate) + '0' + str(timeout)
    hex_data = bytes.fromhex(hex_str)
    print(hex_data)
    ser.write(hex_data)

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

main()