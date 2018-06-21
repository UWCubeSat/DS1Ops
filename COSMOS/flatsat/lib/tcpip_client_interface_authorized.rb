# encoding: ascii-8bit

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

require 'cosmos/interfaces/stream_interface'
require 'cosmos/streams/tcpip_client_stream'

module Cosmos
  # Base class for interfaces that act as a TCP/IP client
  class TcpipClientInterfaceAuthorized < StreamInterface

    # @param hostname [String] Machine to connect to
    # @param write_port [Integer] Port to write commands to
    # @param read_port [Integer] Port to read telemetry from
    # @param write_timeout [Integer] Seconds to wait before aborting writes
    # @param read_timeout [Integer] Seconds to wait before aborting reads
    # @param protocol_type [String] Name of the protocol to use
    #   with this interface
    # @param protocol_args [Array<String>] Arguments to pass to the protocol
     def initialize(
      hostname,
      write_port,
      read_port,
      username,
      password,
      foxid,
      write_timeout,
      read_timeout,
      protocol_type = nil,
      *protocol_args)

      super(protocol_type, protocol_args)

      @hostname = hostname
      @write_port = ConfigParser.handle_nil(write_port)
      @read_port = ConfigParser.handle_nil(read_port)
      @write_timeout = write_timeout
      @username = username
      @password = password
      @foxid = foxid
      @read_timeout = read_timeout
      @read_allowed = false unless @read_port
      @write_allowed = false unless @write_port
      @write_raw_allowed = false unless @write_port
    end

    # Connects the {TcpipClientStream} by passing the
    # initialization parameters to the {TcpipClientStream}.
    def connect
      @stream = TcpipClientStream.new(
        @hostname,
        @write_port,
        @read_port,
        @write_timeout,
        @read_timeout
      )
      super()
	  write_interface @username + "\n"
	  write_interface @password + "\n"
            write_interface @foxid + "\n"
    end
  end
end