require 'cosmos'
require 'cosmos/script'
require 'powerControl'
require 'SDM3065x_scan'
inSun=ask("Time spent in the sun")
inEclipse=ask("Time spent in eclipse")


def cycleChannel(up, cycleTime, voltage, resolution)
	
	if up
                    puts("start up cycle")
		for i in 0..resolution
			v=(voltage*i)/resolution
			setVoltage(1, v)
                              wait(cycleTime/(2*resolution))
                              stat = getStatus
                              wait(cycleTime/(2*resolution))
		end
                    puts("done with up cycle")
	else
                    puts("start down cycle")
		for i in 0..resolution
                              
			v=voltage-(voltage*i)/resolution
                              setVoltage(1, v)
                              wait(cycleTime/(2*resolution))
                              stat = getStatus
                              wait(cycleTime/(2*resolution))
		end
                    puts("done with down cycle")	
	end
end




channelOn(3)
channelOn(1)
setVoltage(3,3.3)

setCurrent(1,1.7)
puts "start"
scanSetup()
setScanRange(2,4)
startScan()
wait(5)
cmd("EPS_DIST DOMSWITCH with PD_COM1 ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_COM2 ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_RAHS ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_BDOT ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_ESTIM ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_WHEELS ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_EPS ENABLE")
wait(1)
cmd("EPS_DIST DOMSWITCH with PD_PPT ENABLE")
wait(1)

while true

  
  for i in 0..120*inSun
    stat = getStatus()
    data = getData(2,4)
    puts "Loop #{i}"
    if data.at(0)<4 and data.at(0).to_f>0
      channelOff(1)
      channelOff(3)
      break
    end    
  end
  
  data = getData(2,4)
  if data.at(0)<4 and data.at(0).to_f>0
    channelOff(1)
    channelOff(3)
    break
  end

  cycleChannel(false, 5.0, 16, 10)
  for i in 0..120*inEclipse
    stat = getStatus()
    data = getData(2,4)
    puts "Loop #{i}"
    if data.at(0)<4 and data.at(0).to_f>0
      channelOff(1)
      channelOff(3) 
      break
    end
  end
  
  data = getData(2,4)
  if data.at(0)<4 and data.at(0).to_f>0
    channelOff(1)
    channelOff(3)
    break
  end
  cycleChannel(true, 5.0, 16, 10)
end