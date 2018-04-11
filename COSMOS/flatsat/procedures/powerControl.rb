require 'cosmos'
require 'cosmos/script'

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



def channelOn(channel)
  cmd("PS_DP832A", "TURN_ON_CHANNEL","channel"=>channel)
end

def channelOff(channel)
  cmd("PS_DP832A", "TURN_OFF_CHANNEL","channel"=>channel)
end

def setVoltage(channel, voltage)
  cmd("PS_DP832A", "SET_VOLTAGE", "voltage" => voltage,"channel"=>channel)
end

def getStatus()
  cmd("PS_DP832A","GETSTATUS")
  v=tlm("PS_DP832A PS_STATUS V_CH1")
  i=tlm("PS_DP832A PS_STATUS i_CH1")
  p=tlm("PS_DP832A PS_STATUS P_CH1")
  chan1 = ChannelStatus.new(v, i, p)
  
  v=tlm("PS_DP832A PS_STATUS V_CH2")
  i=tlm("PS_DP832A PS_STATUS i_CH2")
  p=tlm("PS_DP832A PS_STATUS P_CH2")
  chan2 = ChannelStatus.new(v, i, p)
  
  v=tlm("PS_DP832A PS_STATUS V_CH3")
  i=tlm("PS_DP832A PS_STATUS i_CH3")
  p=tlm("PS_DP832A PS_STATUS P_CH3")
  chan3 = ChannelStatus.new(v, i, p)
  
  stat = StatusPacket.new(chan1, chan2, chan3)
  return stat
end