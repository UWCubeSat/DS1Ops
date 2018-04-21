def scanSetup()
  begin
  cmd("SDM3065X", "SCAN_SET_UP")
  rescue Exception =>e
  puts "WARNING COULD SET UP SCAN"
  end
end

def setScanRange(low, high)
  begin
  for i in low..high+1
        
    cmd("SDM3065X", "TURN_ON_CHANNEL","CHANNEL"=>i)
  end
  
  cmd("SDM3065X", "SET_SCANNING_RANGE","LOW"=>low, "HIGH"=>high)
  rescue Exception =>e
  puts "WARNING COULD NOT SET SCANNING CHANNELS"
  end
end

def startScan()
  begin  
  cmd("SDM3065X", "START_SCAN")
  rescue Exception =>e
  puts "WARNING COULD NOT START SCAN"
  end
end

def endScan()
  begin
  cmd("SDM3065X", "END_SCAN")
  rescue Exception =>e
  puts "WARNING COULD NOT END SCAN"
  end
end

def getData(low, high)
  begin
  data=Array.new(high-low)
  for i in low..high   
    cmd("SDM3065X", "GET_DATA","CHANNEL"=>i)
    
    val=tlm("SDM3065X DATA DATA")
    val=val.gsub(/^[\s>]+/,"")
    val=val.gsub(" VDC", "")
    data[i-low]=val.to_f
    
  end
  rescue Exception =>e
  puts "WARNING COULD NOT GET DATA"
  end
  return data
end