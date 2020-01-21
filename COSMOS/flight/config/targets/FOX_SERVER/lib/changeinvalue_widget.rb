require 'cosmos'
require 'cosmos/tools/tlm_viewer/widgets/value_widget'

module Cosmos

  class ChangeinvalueWidget < ValueWidget
	
    def initialize (parent_layout, target_name, packet_name, item_name, format_string, value_type = :CONVERTED, characters = 12)
	  
      super(parent_layout, target_name, packet_name, item_name, value_type, characters)
      @format_string = format_string
	  @numRecieved = tlm(target_name, packet_name, "RECEIVED_COUNT")
	  @prev_val=0
	  @delta = 0
	  parent_layout.addWidget(self) if parent_layout
    end

    def value= (data)
	  newNumRecieved=tlm(target_name, packet_name,"RECEIVED_COUNT")
	  if newNumRecieved-@numRecieved > 0 
		@delta=data.to_i - @prev_val
		@prev_val=data.to_i
		@numRecieved=newNumRecieved
	  end
      formatted_data = sprintf(@format_string, @delta)
	  
      super(formatted_data)
	  
    end

  end

end # module Cosmos