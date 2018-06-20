# encoding: ascii-8bit

# Copyright 2017 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

require 'cosmos/config/config_parser'
require 'thread'

module Cosmos
  # Creates a CRC on write and verifies a CRC on read
  class CanProtocol < Protocol
	def read_packet(packet)
		if (packet.target_name == "CAN_LOCAL")
			return packet
		else
			return :STOP
		end
	end
  end
end