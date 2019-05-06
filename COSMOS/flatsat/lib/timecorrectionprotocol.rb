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
    @@packet_times = {}
    @@gnd_class_dict = {0 => "gnd_none", 6 => "gnd_health",5 => "gnd_realtime",7 => "gnd_wod",1 => "camera"}
    @@reset_times = {}
    def read_data(data)
      data = super(data)
      if data != :STOP
        #puts("+++++++++++++++++++++++++++++"
        reset = data[4..5].unpack("n")[0]
        uptime =  data[6..9].unpack("N")[0]
        #puts(uptime)
        time = data[12..19].unpack("Q>")[0]
        #mask the whole id, grab just those important 29 bits
        id = (data[24..27].unpack("N")[0] & ((2**30)-1))
        gnd_class = @@gnd_class_dict[(id & (2**22 + 2**21 + 2**20)) >> 20]
        #puts("+++++++++++++++++++++++++++++")
        if gnd_class == "gnd_health"
          if @@reset_times.has_key?(reset)
            if uptime > @@reset_times[reset][0]
              @@reset_times[reset] = [uptime,time]
            end
          else
            @@reset_times[reset]=[uptime,time]
          end
          return data
        elsif gnd_class == "gnd_wod"
          if @@reset_times.has_key?(reset)
            puts(uptime)
            #puts("YES!",id,gnd_class,time,data[12..19],[12345].pack("Q>"))
            data[12..19] = [@@reset_times[reset][1] + uptime*1000 - @@reset_times[reset][0]*1000].pack("Q>")
            #data[12..19] = [100].pack("Q>")
            #puts(data[12..19])
            return data
          else
            return :STOP
          end
        else
          return data
        end
      else
        return data
      end
    end
  end
end

