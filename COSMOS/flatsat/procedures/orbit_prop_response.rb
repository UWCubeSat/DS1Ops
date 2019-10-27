puts "starting"
require 'cosmos'
require 'cosmos/script'

def get_batt_v_max()
    return tlm("AMSAT RC_EPS_DIST_3 RC_EPS_DIST_3_BATT_V_MAX")
end

def get_batt_v_min()
    return tlm("AMSAT RC_EPS_DIST_3 RC_EPS_DIST_3_BATT_V_MIN")
end

def time_since_rc()
 return Time.now.to_i - tlm("AMSAT RC_EPS_DIST_3 PACKET_TIMESECONDS") 
end

def get_mode()
  return tlm("AMSAT COM1_MODE COM1_MODE_MODE")
end

while true
  rise = tlm("ORBIT_PROP PASS rise")
  fall = tlm("ORBIT_PROP PASS fall")
  if rise < 3 and rise > 0
    passing = true
    set to realtime mode
    
    while get_mode != "REAL-TIME_MODE" do
        puts get_mode
        cmd("AMSAT", "GCMD_COM1_MODE_REALTIME", "GCMD_COM1_MODE_REALTIME_TIME"=>10)
        sleep(30)    
    end
   puts(get_mins)
   reset mins and maxs 
    old_diff = get_batt_v_max - get_batt_v_min
    diff = get_batt_v_max - get_batt_v_min
    
    while diff <= old_diff do
      sleep(40)
      puts('looping')
      cmd("AMSAT", "GCMD_RESET_MINMAX", "GCMD_RESET_MINMAX_BDOT"=>1, "GCMD_RESET_MINMAX_PPT"=>1, "GCMD_RESET_MINMAX_DIST"=>1, "GCMD_RESET_MINMAX_GEN"=>1, "GCMD_RESET_MINMAX_BATT"=>1, "GCMD_RESET_MINMAX_ESTIM"=>1, "GCMD_RESET_MINMAX_MPC"=>1, "GCMD_RESET_MINMAX_SENSORPROC"=>1, "GCMD_RESET_MINMAX_MTQ"=>1)
      while time_since_rc > 4
        puts time_since_rc
        sleep(4)
      end
        
  
      old_diff = diff
      diff = get_batt_v_max - get_batt_v_min
      
    end


    #send commands in file
    File.open("procedures/cmd.txt", "r") do |f|
      f.each_line do |line|
        cmd(line)
      end
    end
  end
  
sleep(3)
end