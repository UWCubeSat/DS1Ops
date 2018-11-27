

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
  def initialize(chan1, chan2, chan3)
    @chan1 = chan1
    @chan2 = chan2
    @chan3 = chan3
  end
  
  def voltage(channel)
    if channel == 1
      return @chan1.voltage()
    end
    if channel == 2
      return @chan2.voltage()
    end
    if channel == 3
      return @chan3.voltage()
    end
  end
  
  def current(channel)
    if channel == 1
      return @chan1.current()
    end
    if channel == 2
      return @chan2.current()
    end
    if channel == 3
      return @chan3.current()
    end
  end
  
  def power(channel)
    if channel == 1
      return @chan1.power()
    end
    if channel == 2
      return @chan2.power()
    end
    if channel == 3
      return @chan3.power()
    end
  end
  
end


class DP811A
def self.channelOn(channel)
  begin 
  cmd("PS_DP811A", "TURN_ON_CHANNEL","channel"=>channel)
  rescue Exception =>e
  puts "WARNING COULD NOT UPDATE VOLTAGE"
  end
end

def self.channelOff(channel)
  begin
  cmd("PS_DP811A", "TURN_OFF_CHANNEL","channel"=>channel)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN OFF CHANNEL"
  end
end

def self.setVoltage(channel, voltage)
  begin
  cmd("PS_DP811A", "SET_VOLTAGE", "voltage" => voltage,"channel"=>channel)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON CHANNEL"
  end
end

def self.setCurrent(channel, current)
  begin
  cmd("PS_DP811A", "SET_CURRENT", "current" => current,"channel"=>channel)
  rescue Exception =>e
  puts "WARNING COULD NOT SET CURRENT"
  end
end

def self.isChannelOn(channel)
  begin
  cmd("PS_DP811A","GETCHANNELSTATE", "channel"=>channel)
  state=tlm("PS_DP811A CH#{channel}_STATE STATE")
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
  chan1 = ChannelStatus.new(v, i, p)
  
  v=tlm("PS_DP811A PS_STATUS V_CH2")
  i=tlm("PS_DP811A PS_STATUS i_CH2")
  p=tlm("PS_DP811A PS_STATUS P_CH2")
  chan2 = ChannelStatus.new(v, i, p)
  
  v=tlm("PS_DP811A PS_STATUS V_CH3")
  i=tlm("PS_DP811A PS_STATUS i_CH3")
  p=tlm("PS_DP811A PS_STATUS P_CH3")
  chan3 = ChannelStatus.new(v, i, p)
  
  stat = StatusPacket.new(chan1, chan2, chan3)
  rescue Exception => e
  stat = nil
  puts "WARNING COULD NOT GET STATUS"
  end
  return stat
end

def self.setOverVoltage(voltage)
  begin
  cmd("PS_DP811A", "SET_OOVER_VOLTAGE", "voltage" => voltage,"channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT SET OVER VOLTAGE"
  end
end

def self.setOverCurrent(current)
  begin
  cmd("PS_DP811A", "SET_OOVER_CURRENT", "current" => voltage,"channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT SET OVER VOLTAGE"
  end
end

def self.overVoltageOff()
  begin
  cmd("PS_DP811A", "TURN_OFF_OVER_VOLTAGE","channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN OFF OVERVOLTAGE"
  end
end

def self.overVoltageOn()
  begin
  cmd("PS_DP811A", "TURN_ON_OVER_VOLTAGE","channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON OVERVOLTAGE"
  end
end

def self.overCurrentOff()
  begin
  cmd("PS_DP811A", "TURN_OFF_OVER_CURRENT","channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN OFF OVERCURRENT"
  end
end

def self.overCurrentOn()
  begin
  cmd("PS_DP811A", "TURN_ON_OVER_Current","channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON OVERCURRENT"
  end
end

def self.senseOn()
  begin
  cmd("PS_DP811A", "TURN_ON_SENSE","channel"=>1)
  rescue Exception =>e
  puts "WARNING COULD NOT TURN ON SENSE"
  end
end
end