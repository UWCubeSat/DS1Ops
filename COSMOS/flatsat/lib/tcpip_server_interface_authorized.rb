# encoding: ascii-8bit

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

require 'socket'
require 'thread' # For Mutex
require 'timeout' # For Timeout::Error
require 'cosmos/interfaces/stream_interface'
require 'cosmos/streams/tcpip_socket_stream'
require 'cosmos/config/config_parser'

module Cosmos

	# TCP/IP Server which can both read and write on a single port or two
	# independent ports. A listen thread is setup which waits for client
	# connections. For each connection to the read port, a thread is spawned that
	# calls the read method from the interface. This data is then
	# available by calling the TcpipServer read method. For each connection to the
	# write port, a thread is spawned that calls the write method from the
	# interface when data is send to the TcpipServer via the write method.
	class TcpipServerInterfaceAuthorized < TcpipServerInterface
	# Data class which stores the interface and associated information
		def connect
			sock = TCPSocket.new('localhost', 8081)
			sock.write 'GUEST\namsattest\n'
			sock.close
			super()
		end
	end
end