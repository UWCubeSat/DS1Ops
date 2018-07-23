require 'cosmos'
require 'cosmos/tools/tlm_viewer/widgets/value_widget'

module Cosmos

  class DifferenceWidget < ValueWidget
	
    def initialize (parent_layout, target_name, packet_name, item_name,target_name2, packet_name2, item_name2, value_type = :CONVERTED, characters = 12)
	  
      super(parent_layout, target_name, packet_name, item_name, value_type, characters)
      
	  @target=target_name2
	  @packet = packet_name2
	  @item = item_name2
	  
	  parent_layout.addWidget(self) if parent_layout
    end

    def value= (data)
	  val=data.to_f-tlm(@target, @packet, @item).to_f
	  formatted_data="#{val}"
      super(formatted_data)
	  
    end

  end

end # module Cosmos