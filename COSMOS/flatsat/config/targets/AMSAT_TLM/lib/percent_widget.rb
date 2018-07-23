require 'cosmos'
require 'cosmos/tools/tlm_viewer/widgets/value_widget'

module Cosmos

  class PercentWidget < ValueWidget
	
    def initialize (parent_layout, target_name, packet_name, item_name, max_val,value_type = :CONVERTED, characters = 12)
	  
      super(parent_layout, target_name, packet_name, item_name, value_type, characters)
      @max_val=max_val.to_f
	  parent_layout.addWidget(self) if parent_layout
    end

    def value= (data)
	  percent=100*data.to_f/@max_val
	  formatted_data="#{percent}%"
      super(formatted_data)
	  
    end

  end

end # module Cosmos