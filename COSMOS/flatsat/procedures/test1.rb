require 'csv'
load 'loadControl.rb'
load 'PS_DP811A_Control.rb'

file_name = ask("Output file name")
file = CSV.open(file_name,'w')
puts file
file << ["time", "voltage", "current"]
DP811A.setOverVoltage(3.7)
DP811A.setOverCurrent(2)
DP811A.overVoltageOn
DP811A.overCurrentOn
DP811A.senseOn
Load.senseOn

v = Load.getVoltage()[1]
i = Load.getCurrent()[1]
if v>1 and v<3.5
	file << ["time", "voltage", "current"]
	DP811A.channelOn
	DP811A.setCurrent(1.5)
	DP811A.setVoltage(3.7)
	while v<3.6
		time, v = Load.getVoltage
		i = Load.getCurrent[1]
		file << [time, v, i]
	end
	DP811A.setVoltage(3.6)
	DP811A.setCurrent(2)
	while i > 0.0011
		time, v = Load.getVoltage
		i = Load.getCurrent[1]
		file << [time, v, i]
	end
end
file.close()