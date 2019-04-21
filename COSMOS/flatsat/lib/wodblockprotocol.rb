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
  class Wodblockprotocol < Protocol
    @@packet_times = {}
    @@gnd_class_dict = {0 => "gnd_none", 6 => "gnd_health",5 => "gnd_realtime",7 => "gnd_wod",1 => "camera"}
    def read_data(data)
      data = super(data)
      if data != :STOP
        #puts("+++++++++++++++++++++++++++++"
        reset = data[4..5].unpack("n")[0]
        uptime =  data[6..9].unpack("n")[0]
        #mask the whole id, grab just those important 29 bits
        id = (data[24..27].unpack("N")[0] & ((2**30)-1))
        gnd_class = @@gnd_class_dict[(id & (2**22 + 2**21 + 2**20)) >> 20]
        #if (id & (2**22 + 2**21 + 2**20)) >> 20 == 6
          #puts(id,gnd_class)
        #end
        #puts("+++++++++++++++++++++++++++++")

        if @@packet_times.has_key?(id)
          if (reset >= @@packet_times[id][0] and uptime > @@packet_times[id][1])
            @@packet_times[id] = [reset,uptime]
            puts("YES!",id,gnd_class)
            return data
          else
            puts("NO!",id,gnd_class)
            return :STOP
          end
        else
          @@packet_times[id] = [reset,uptime]
          return data
        end
      else
        return data
      end
    end
  end
end

