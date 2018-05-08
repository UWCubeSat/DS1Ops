load "powerControl.rb"
while true
if !isChannelOn(1)
  puts "----------WARNING CHANNEL 1 WAS OFF, TURNING BACK ON-----------"
  channelOn(1)
end
wait(0.5)
if !isChannelOn(3)
  puts "----------WARNING CHANNEL 3 WAS OFF, TURNING BACK ON-----------"
  channelOn(3)
end
wait(0.5)
end