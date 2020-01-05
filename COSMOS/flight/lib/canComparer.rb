require 'cosmos'
require 'cosmos/interfaces/tcpip_client_interface'
require 'yaml'
i = Cosmos::TcpipClientInterface.new('192.168.1.152',7779,7779,nil,nil,'PREIDENTIFIED')
i.connect

STDOUT.sync = true

$peak_dict = { }
$amsat_dict = {}

def addToDict(hmap,k)
	if hmap.key?(k) then
		hmap[k] = hmap[k] + 1
	else
		hmap[k] = 1
	end
end

trap("INT") {
}

Thread.new {
	loop do
		puts $peak_dict
		$peak_dict.each_key do |k|
			puts(Time.now)
			if $amsat_dict.key?(k) then
				if $amsat_dict[k] != $peak_dict[k] then
		    	puts k
					print("---------\n")
					print("AMSAT: " , $amsat_dict[k].to_s ," \n")
					print("PEAK: " , $peak_dict[k].to_s , " \n")
					print("---------\n")
				end
			else 
	    	puts k
				print("---------\n")
			print("AMSAT: 0 , \n")
			print("PEAK: " , $peak_dict[k].to_s, " \n")
				print("---------\n")
			end
		end
		sleep(60)
	end
}
Thread.new {
	loop do
		pkt = i.read
		if pkt.target_name == "PEAK_CAN" then 
			# puts $peak_dict
			addToDict($peak_dict,pkt.packet_name)
		end
		if pkt.target_name == "AMSAT" then 
			addToDict($amsat_dict,pkt.packet_name)
		end
	end
}
loop do
	puts("PRESS 's' TO WRITE DATA AND EXIT TO FILE AT ANY TIME")
	char = STDIN.getc
	if char == "s" then
		puts("writing to file...")
		File.write('outMaps.yml', [$peak_dict,$amsat_dict].to_yaml)
		puts("exiting")
		exit()
	end

end


