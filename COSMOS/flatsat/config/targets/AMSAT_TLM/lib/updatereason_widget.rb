require 'cosmos'
require 'cosmos/tools/tlm_viewer/widgets/value_widget'

module Cosmos

  class UpdatereasonWidget < ValueWidget
	
    def initialize (parent_layout, target_name, packet_name, item_name,value_type = :CONVERTED, characters = 25)
	  
      super(parent_layout, target_name, packet_name, item_name, value_type, characters)
      @reasons = Hash[0 => "None",
						2 => "Brownout",
						4 => "RST/NMI",
						6 => "PMMSWBOR",
						8 => "Wakeup from LPMx.5",
						10 => "Security violation",
						12 => "SVSL",
						14 => "SVSH",
						16 => "SVML_OVP",
						18 => "SVMH_OVP",
						20 => "PMMSWPOR",
						22 => "WDT time out",
						24 => "WDT password violation",
						26 => "Flash password violation",
						28 => "Reserved",
						30 => "PERF peripheral/configuration area fetch",
						32 => "PMM password violation"]
	  parent_layout.addWidget(self) if parent_layout
    end

    def value= (data)
	  formatted_data="#{@reasons[data.to_i]}"
      super(formatted_data)
	  
    end

  end

end # module Cosmos