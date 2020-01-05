

class ChannelStatus
  def initialize(v, i, p)
    @voltage = v
    @current = i
    @power = p
  end
  def voltage
    return @voltage
  end
  def current
    return @current
  end
  def power
    return @power
  end
end

class StatusPacket
  def initialize(chan1)
    @chan1 = chan1
  end
  
  def voltage
     return @chan1.voltage()
  end
  
  def current
     return @chan1.current()
  end
  
  def power
     return @chan1.power()
  end
  
end


class DP811A
def self.channelOn
  begin 
  cmd("PS_DP811A", "TURN_ON_CHANNEL","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT UPDATE VOLTAGE"
  end
end

def self.channelOff
  begin
  cmd("PS_DP811A", "TURN_OFF_CHANNEL","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN OFF CHANNEL"
  end
end

def self.setVoltage( voltage)
  begin
  cmd("PS_DP811A", "SET_VOLTAGE", "VOLTAGE" => voltage,"CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON CHANNEL"
  end
end

def self.setCurrent(current)
  begin
  cmd("PS_DP811A", "SET_CURRENT", "CURRENT" => current,"CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT SET CURRENT"
  end
end

def self.isChannelOn
  begin
  cmd("PS_DP811A","GETCHANNELSTATE", "CHANNEL"=>1)
  state=tlm("PS_DP811A CH#{1}_STATE STATE")
  if state == "ON"
    return true
  end
  return false
  rescue Exception =>e
  puts "WARNING COULD CHECK CHANNEL STATUS"
  end
end

def self.getStatus()
  begin 
  cmd("PS_DP811A","GETSTATUS")
  v=tlm("PS_DP811A PS_STATUS V_CH1")
  i=tlm("PS_DP811A PS_STATUS i_CH1")
  p=tlm("PS_DP811A PS_STATUS P_CH1")
  time = tlm("PS_DP811A PS_STATUS PACKET_TIMESECONDS")
  chan1 = ChannelStatus.new(v, i, p)
  
  stat = StatusPacket.new(chan1)
  return [time, stat] 
  rescue Exception => e
  puts "WARNING COULD NOT GET STATUS"
  return [0, nil]
  end
  
end

def self.getCurrent
begin 
  cmd("PS_DP811A","GETSTATUS")
  
  i=tlm("PS_DP811A PS_STATUS i_CH1")
 
  time = tlm("PS_DP811A PS_STATUS PACKET_TIMESECONDS")
  
  
  
  return [time, i] 
  rescue Exception => e
  puts "WARNING COULD NOT GET STATUS"
  return [0, 0]
  end
end


def self.setOverVoltage(voltage)
  begin
  cmd("PS_DP811A", "SET_OVER_VOLTAGE", "VOLTAGE" => voltage,"CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT SET OVER VOLTAGE"
  end
end

def self.setOverCurrent(current)
  begin
  cmd("PS_DP811A", "SET_OVER_CURRENT", "CURRENT" => current,"CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT SET OVER CURRENT"
  end
end

def self.overVoltageOff()
  begin
  cmd("PS_DP811A", "TURN_OFF_OVER_VOLTAGE","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN OFF OVERVOLTAGE"
  end
end

def self.overVoltageOn()
  begin
  cmd("PS_DP811A", "TURN_ON_OVER_VOLTAGE","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON OVERVOLTAGE"
  end
end

def self.overCurrentOff()
  begin
  cmd("PS_DP811A", "TURN_OFF_OVER_CURRENT","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN OFF OVERCURRENT"
  end
end

def self.overCurrentOn()
  begin
  cmd("PS_DP811A", "TURN_ON_OVER_Current","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON OVERCURRENT"
  end
end

def self.senseOn()
  begin
  cmd("PS_DP811A", "TURN_ON_SENSE","CHANNEL"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON SENSE"
  end
end
end