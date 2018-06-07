def turnOn()
	begin
		cmd("DIGITAL_LOAD", "TURN_ON")
	rescue exception =>e
		puts "WARNING. COULD NOT TURN ON INPUT"
	end
end

def turnOff()
	begin
		cmd("DIGITAL_LOAD", "TURN_OFF")
	rescue exception =>e
		puts "WARNING. COULD NOT TURN OFF INPUT"
	end
end

def setConstantCurrentMode()
	begin
		cmd("DIGITAL_LOAD", "SET_CONSTANT_CURRENT_MODE")
	rescue exception =>e
		puts "WARNING. COULD NOT SET CONSTANT CURRENT MODE"
	end
end

def setConstantVoltageMode()
	begin
		cmd("DIGITAL_LOAD", "SET_CONSTANT_VOLTAGE_MODE")
	rescue exception =>e
		puts "WARNING. COULD NOT SET CONSTANT VOLTAGE MODE"
	end
end

def setConstantPowerMode()
	begin
		cmd("DIGITAL_LOAD", "SET_CONSTANT_POWER_MODE")
	rescue exception =>e
		puts "WARNING. COULD NOT SET CONSTANT POWER MODE"
	end
end

def setConstantResistanceMode()
	begin
		cmd("DIGITAL_LOAD", "SET_CONSTANT_RESISTANCE_MODE")
	rescue exception =>e
		puts "WARNING. COULD NOT SET CONSTANT RSISTANCE MODE"
	end
end