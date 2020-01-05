def change_index(thewindow)
	puts thewindow.class.name.to_s
	comboBox = thewindow.get_named_widget('mode_combo')
	comboBox.setCurrentIndex(2);
end

#require 'cosmos/tools/tlm_viewer/widgets/timegraph_widget'
require 'time'
require 'cosmos/tools/tlm_viewer/widgets/linegraph_widget'
require 'cosmos/script'
newGraph = Cosmos::LinegraphWidget.new(