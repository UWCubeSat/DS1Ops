require 'csv'
load 'loadControl.rb'
load 'PS_DP811A_Control.rb'

file_name = ask("Output file name")
file = CSV.open(file_name,'w')
puts file
file << ["time (s)", "voltage (V)", "current (A)"]
DP811A.setOverVoltage(3.65)
DP811A.setOverCurrent(1.6)
DP811A.overVoltageOn
DP811A.overCurrentOn

DP811A.senseOn
Load.senseOn

v = Load.getVoltage()[1]

puts v


if v>1 and v<3.5
	
	
	DP811A.setCurrent(1.5)
	DP811A.setVoltage(3.6)
          DP811A.channelOn
          sleep 1
          rsp = DP811A.getStatus()
          startTime = rsp[0]
          i = rsp[1].current
          puts startTime

	while i > 0.011
		rsp= Load.getVoltage
                    time = rsp[0]
                    v = rsp[1]
                    
		i = DP811A.getStatus()[1].current
		file << [time-startTime, v, i]
                    sleep 0.7
	end
end
DP811A.channelOff
Load.turnOff
file.close()
temp = ask("Test complete")
