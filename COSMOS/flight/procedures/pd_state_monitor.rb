@@pdNums = { "COM2" => "6", "RAHS" => "8", "BDOT" => "10", "ESTIM" => "12", "EPS" => "14", "PPT" => "16"}

#~ get power domain status by name string
def getPdState(pd)
  return tlm("peak_can rc_eps_dist_" + @@pdNums[pd] + " rc_eps_dist_" + @@pdNums[pd] + "_" + pd + "_STATE")  
end

#~ populate dictionary with latest pd states
def updatePdVals(dict)
  dict.each do |key, value|
    dict[key] = getPdState(key)
  end
end

#~ Start of script
puts "__________________________"
puts "Starting PD Monitor Script"
puts "**************************"

#~ initializing previous states
prevState = {"COM2" => "", "RAHS" => "", "BDOT" => "", "ESTIM" => "", "EPS" => "", "PPT" => ""}
currState = {"COM2" => "", "RAHS" => "", "BDOT" => "", "ESTIM" => "", "EPS" => "", "PPT" => ""}

#~ uncomment this line to make the script not print out the initial pd states
#updatePdVals(prevState)

loop do
  updatePdVals(currState)
  currState.each do |key, value|
    if(value != prevState[key])
      puts key + ": " + value
      prevState[key] = value
    end
  end
end