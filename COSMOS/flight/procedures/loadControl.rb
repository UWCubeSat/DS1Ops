class Load
def self.turnOn()
  begin
    cmd("DIGITAL_LOAD", "TURN_ON")
  rescue Exception =>e
    puts "WARNING. COULD NOT TURN ON INPUT"
  end
end

def self.isOn()
  begin
    cmd("DIGITAL_LOAD", "GET_INPUT_STATE")
    
    state= tlm("DIGITAL_LOAD STATUS STATE")
    time = tlm("DIGITAL_LOAD STATUS PACKET_TIMESECONDS")
    if state == 1
      return [time, true]
    else
      return [time, false]
    end
  rescue Exception =>e
    puts "WARNING. COULD NOT GET INPUT STATE"
  end
end

def self.turnOff()
  begin
    cmd("DIGITAL_LOAD", "TURN_OFF")
  rescue Exception =>e
    puts "WARNING. COULD NOT TURN OFF INPUT"
  end
end

def self.setConstantCurrentMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_CURRENT_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT CURRENT MODE"
  end
end

def self.setConstantVoltageMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_VOLTAGE_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT VOLTAGE MODE"
  end
end

def self.setConstantPowerMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_POWER_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT POWER MODE"
  end
end

def self.setConstantResistanceMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_RESISTANCE_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT RSISTANCE MODE"
  end
end

def self.setCurrentLevel(i)
  begin
    cmd("DIGITAL_LOAD", "SET_CURRENT", "current"=>i)
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CURRENT LEVEL"
  end
end

def self.setVoltageLimit(v)
  begin
    cmd("DIGITAL_LOAD", "SET_VOLTAGE_LIMIT", "voltage"=>v)
  rescue Exception => e
    puts "WARNING. COULD NOT SET VOLTAGE LIMIT"
  end
end

def self.isVoltageBelow(limit)
  begin
    cmd("DIGITAL_LOAD GET_VOLTAGE")
    v = tlm("DIGITAL_LOAD INPUT_VOLTAGE V")
	time = tlm("DIGITAL_LOAD INPUT_VOLTAGE PACKET_TIMESECONDS")
    if v< limit
      return [time, true]
    else
      return [time, false]
    end
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT VOLTAGE"
  end
end

def self.getCurrent()
  begin
    cmd("DIGITAL_LOAD GET_CURRENT")
    time = tlm("DIGITAL_LOAD INPUT_CURRENT PACKET_TIMESECONDS")
    i = tlm("DIGITAL_LOAD INPUT_CURRENT I")
    return [time, i]
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT CURRENT"
	return [0,0]
  end
end

def self.getVoltage()
  begin
    cmd("DIGITAL_LOAD GET_VOLTAGE")
    v = tlm("DIGITAL_LOAD INPUT_VOLTAGE V")
    time = tlm("DIGITAL_LOAD INPUT_VOLTAGE PACKET_TIMESECONDS")
   
    return [time, v]
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT VOLTAGE"
	return [0, 0]
  end
end
def self.senseOn()
  begin
    cmd("DIGITAL_LOAD ENABLE_SENSE")
  rescue Exception => e
    puts "WARNING. COULD NOT ENABLE SENSE"
  end
end

end