# this script listens to can data from localhost:1235 and outputs only processed wod data on localhost:1255
# what "processed wod" data means is still being determined

import socket
import struct

last_wod_uptimes = {}

def bytes_to_int(bytes):
	# https://stackoverflow.com/a/39713066
	return reduce(lambda s, x: s*256 + x, bytearray(bytes))

if __name__ == "__main__":
	recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	recv_sock.connect(('localhost', 1235))
	send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_sock.connect(('localhost', 1255))
	
	try:
		while True:
			# get string out for debugging with packet.encode("hex")
			packet     = recv_sock.recv(36)
			id         = bytes_to_int(packet[24:28])
			grnd_class = (id >> 20) & 7
			reset      = bytes_to_int(packet[4:6])
			uptime     = bytes_to_int(packet[6:10])
			
			# added the explicit id for COM1_MODE
			if (grnd_class == 7 or id == 302252858) and (not (id in last_wod_uptimes) or
																		(uptime > last_wod_uptimes[id][1] and reset == last_wod_uptimes[id][0]) or
																		reset > last_wod_uptimes[id][0]):
				send_sock.send(packet)
				last_wod_uptimes[id] = (reset, uptime)
	finally:
		recv_sock.close()
