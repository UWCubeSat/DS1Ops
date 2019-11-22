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
  # Base class for all COSMOS protocols which defines a framework which must be
  # implemented by a subclass.
  class Timecorrectionprotocol < Protocol
    def read_data(data)
      data = super(data)
      if data != :STOP
        id = (data[24..27].unpack("N")[0] & ((2**30)-1))
        gnd_class = (id & (2**22 + 2**21 + 2**20)) >> 20
        if gnd_class != 7
          # block all non-WOD
          return :STOP
        end
      end
      return data
    end
  end
end

