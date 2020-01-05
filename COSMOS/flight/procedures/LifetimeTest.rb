#Cycle testing procedure for battery board
#Author: Jamie, sean

require "loadControl"

#setVoltageLimit(4)

#This is the cycle test part
100.times do

  #If charged, then discharge
  if tlm("EPS_BATT SENSORDAT BATTERYVOLT") > 6.9 and tlm("EPS_BATT SENSORDAT BATTERYCURR") < 0.1
    puts "Battery is full!"
    cmd("EPS_GEN CHARGECMD with PT1_ENABLECHARGE DISABLE, PT2_ENABLECHARGE DISABLE, PT3_ENABLECHARGE DISABLE")#disable charge
    #Makes sure the load turns on   
    while !isOn()   
      setCurrentLevel(4)
      sleep 1
      turnOn()
      sleep 1
    end
    loop do 
      break if tlm("EPS_BATT SENSORDAT BATTERYVOLT") < 5
    end 
    puts "Battery is empty!"
    
  #If not charged, then charge
  else 
    puts "Battery is charging!"
     while isOn()
       turnOff()
     end
     cmd("EPS_GEN CHARGECMD with PT1_ENABLECHARGE ENABLE, PT2_ENABLECHARGE ENABLE, PT3_ENABLECHARGE ENABLE")   
    loop do 
      break if tlm("EPS_BATT SENSORDAT BATTERYVOLT") > 6.9 and tlm("EPS_BATT SENSORDAT BATTERYCURR") < 0.1                                                                                                                                         
    end
    puts "Battery has been charged!"  
  end 
end

#if the script ends turn off the load and but keep charging to make sure that the batteries don't drain themselves.
turnoff()