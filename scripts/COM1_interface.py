import serial.serialwin32
import sys
import time #TODO: remove
import threading

softwarePort = 256

def main():
	print("BootloaderNotFound")
	threads = []
	for i in range(256):
		t = threading.Thread(target=tryBootOnPort, args=(i,))
		threads.append(t)
		t.start()
		t.join()

def tryBootOnPort(portNum):
	portIsBootloader = False
	try:
		bootloader = serial.Serial('COM' + str(portNum), timeout=1)
		if (isBootloader(bootloader)):
			bootloader.write(b"a")
			#print('Successfully exited bootloader on COM' + str(portNum))
			portIsBootloader = True
	except:
		return

	while(portIsBootloader):
		try:
			software = serial.Serial('COM' + str(portNum + 1), timeout=1)
			software.write(b'ignore umbilical\r\n')
			print("ignore umbilical")
			software.write(b'health mode\r\n')
			print("health mode")
			software.write(b'transponder disable\r\n')
			print("transponder disable")
			#print("Software initialized on COM" + str(portNum + 1))
			print("COM" + str(portNum+1))
			return
		except:
			pass

def isBootloader(ser):
	ser.write(b"v")
	return ser.readline() == b'altos-loader\r\n'

main()