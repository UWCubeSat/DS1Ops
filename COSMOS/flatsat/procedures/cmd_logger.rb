

ignore = ['LENGTH', 'FIXED_TYPE', 'TAG', 'TIMESTAMP_L', 'TIMESTAMP_H', 'CHANNEL', 'DLC', 'FLAGS', 'CANID_PADDING', 'CANID_RTR', 'CANID_TYPE', 'CANID', 'PADDING']
times = Hash.new()
first_cmd = false
for c in get_cmd_list "AMSAT_CMD"
  times.store(c, get_cmd_time("AMSAT_CMD", c[0])[2])
end

while true
  last = get_cmd_time("AMSAT_CMD")[2]
  while last == nil
    sleep 10
    last = get_cmd_time("AMSAT_CMD")[2]
    first_cmd = true
  end
  while get_cmd_time("AMSAT_CMD")[2] <= last and not first_cmd
    sleep 10
  end
  first_cmd = false
  updates = []
  for c in get_cmd_list "AMSAT_CMD"
    if  times[c] != get_cmd_time("AMSAT_CMD", c[0])[2]
      updates.push([c[0], get_cmd_time("AMSAT_CMD")[2]])
    end
   end
   
   updates = updates.sort_by{|i| i[1]}
   
   for u in updates  
     print_out = "#{u[1]} "+u[0] +" with "
     for p in get_cmd_param_list "AMSAT_CMD", u[0]
       if not ignore.include? p[0]
          print_out += p[0]
          print_out += " = "
          print_out += "#{get_cmd_value "AMSAT_CMD", u[0], p[0]}"
          print_out += '  '
       end
     end
     puts print_out
   end
  
  for c in get_cmd_list "AMSAT_CMD"
    times.store(c, get_cmd_time("AMSAT_CMD", c[0])[2]) 
  end
end