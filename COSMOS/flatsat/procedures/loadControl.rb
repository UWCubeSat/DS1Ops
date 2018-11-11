class Load
def turnOn()
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
   
    if state == 1
      return true
    else
      return false
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
    if v< limit
      return true
    else
      return false
    end
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT VOLTAGE"
  end
end

def self.getCurrent()
  begin
    cmd("DIGITAL_LOAD GET_CURRENT")
    i = tlm("DIGITAL_LOAD INPUT_CURRENT I")
    return i
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT CURRENT"
	return nil
  end
end

def self.getVoltage()
  begin
    cmd("DIGITAL_LOAD GET_CURRENT")
    v = tlm("DIGITAL_LOAD INPUT_VOLTAGE V")
    return v
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT CURRENT"
	return nil
  end
end

def self.getCurrent()
  begin
    cmd("DIGITAL_LOAD ENABLE_SENSE")
    i = tlm("DIGITAL_LOAD INPUT_CURRENT I")
    return i
  rescue Exception => e
    puts "WARNING. COULD NOT GET INPUT CURRENT"
	return nil
  end
end

end