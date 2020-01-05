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
  class Wodblockprotocol < Protocol

    def initialize(allow_empty_data = nil)
      super()
      @last_wod_uptime = -1.0/0
      @last_wod_reset  = -1.0/0
      @last_wod_data   = :STOP
    end

    def read_data(data)
      data = super(data)
      if data != :STOP
        id = (data[24..27].unpack("N")[0] & ((2**30)-1))
        gnd_class = (id & (2**22 + 2**21 + 2**20)) >> 20
        
        if gnd_class == 7  # this is WOD
          reset = data[4..5].unpack("n")[0]
          uptime =  data[6..9].unpack("N")[0]
          if uptime < @last_wod_uptime && reset == @last_wod_reset
            # this packet is older, so pass the last one
            new_data = data
            data = @last_wod_data
            @last_wod_data = new_data
          else
            @last_wod_data = data
            data = :STOP
          end
          @last_wod_uptime = uptime
          @last_wod_reset  = reset
        end
      end
      return data
    end
  end
end

