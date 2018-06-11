def turnOn()
  begin
    cmd("DIGITAL_LOAD", "TURN_ON")
  rescue Exception =>e
    puts "WARNING. COULD NOT TURN ON INPUT"
  end
end

def isOn()
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

def turnOff()
  begin
    cmd("DIGITAL_LOAD", "TURN_OFF")
  rescue Exception =>e
    puts "WARNING. COULD NOT TURN OFF INPUT"
  end
end

def setConstantCurrentMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_CURRENT_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT CURRENT MODE"
  end
end

def setConstantVoltageMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_VOLTAGE_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT VOLTAGE MODE"
  end
end

def setConstantPowerMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_POWER_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT POWER MODE"
  end
end

def setConstantResistanceMode()
  begin
    cmd("DIGITAL_LOAD", "SET_CONSTANT_RESISTANCE_MODE")
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CONSTANT RSISTANCE MODE"
  end
end

def setCurrentLevel(i)
  begin
    cmd("DIGITAL_LOAD", "SET_CURRENT", "current"=>i)
  rescue Exception =>e
    puts "WARNING. COULD NOT SET CURRENT LEVEL"
  end
end

def setVoltageLimit(v)
  #begin
    cmd("DIGITAL_LOAD", "SET_VOLTAGE_LIMIT", "voltage"=>v)
  #rescue Exception => e
  #  puts "WARNING. COULD NOT SET VOLTAGE LIMIT"
  #end

end