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
require 'timeout'

module Cosmos
  # Base class for interfaces that act as a TCP/IP client
  class TcpipClientInterfaceBuffered < TcpipClientInterface

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
      write_timeout,
      read_timeout,
      protocol_type = nil,
      *protocol_args)

      super(hostname, write_port, read_port, write_timeout, read_timeout, protocol_type = nil, *protocol_args)

      @buffer = Queue.new
      # the number of reads without data
      @error = false
      Thread.new {
        loop do
          begin
            if @stream.connected?
              data = @stream.read
              #puts "read some data of len: " + data.length.to_s
              if data.length == 3
                 @error = false
                if data == "\x00\x03\x00"
                  # we're good to go!
                  # "\x00\x03\x01" means that AmCom is transmitting
                  unless @buffer.empty?
                    packet = @buffer.pop
                    method(:write_interface).super_method.call(packet)
                  end
                end
              else
                # length error
                @error = @error || true
              end
            end
          rescue => e
            puts "ERROR: " + e.to_s
          end
        sleep(0.1)
        end
      }
    end
  
    def read_interface
      while !@error
      end
      # this return indictates that the connection should be closed
      return nil
    end

    def connect
      @error = false
      super()
    end

    def disconnect
      super()
      @buffer.clear
    end

    def write_interface(data)
        @buffer << data
    end
  end
end