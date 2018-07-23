
module Cosmos
  # Base class for interfaces that act as a TCP/IP client
  class CanFusion < TcpipClientInterface 
 	def initialize(hostname,
		           write_port,
		           read_port,
		           write_timeout,
		           read_timeout,
		           stream_protocol_type,
		           *stream_protocol_args)
		super(hostname,write_port,read_port,write_timeout,read_timeout,stream_protocol_type,*stream_protocol_args)

		@i=0	
    end
    def read
    	packet = super()
    	# print("boop town boiz")
    	# packet.received_time()
    	# @i = @i +1
    	# packet.received_time=Time.new(2020,1,31,12,30,59-(@i % 60))
    	return packet
    end
  end
end