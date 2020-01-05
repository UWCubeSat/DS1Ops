require 'cosmos'
require 'cosmos/tools/tlm_viewer/widgets/value_widget'

module Cosmos

  class LastupdateWidget < ValueWidget
	
    def initialize (parent_layout, target_name, packet_name, item_name, value_type = :CONVERTED, characters = 12)
	  
      super(parent_layout, target_name, packet_name, item_name, value_type, characters)
      
	  @numRecieved = tlm(target_name, packet_name, "RECEIVED_COUNT")
	  @prev_val=tlm(target_name, packet_name, item_name)
	  @formatted_data = "Before Monitoring Began"
	  parent_layout.addWidget(self) if parent_layout
    end

    def value= (data)
	  newNumRecieved=tlm(target_name, packet_name,"RECEIVED_COUNT")
	  if newNumRecieved-@numRecieved > 0 
		delta=data.to_i - @prev_val
		@prev_val=data.to_i
		@numRecieved=newNumRecieved
		if delta !=0 
			time = tlm(target_name, packet_name, "RECEIVED_TIMEFORMATTED")
			@formatted_data = time
		end
	  end
      
	  
      super(@formatted_data)
	  
    end

  end

end # module Cosmos