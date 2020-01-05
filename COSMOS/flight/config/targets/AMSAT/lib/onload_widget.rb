require 'cosmos/tools/tlm_viewer/widgets/widget'
require 'cosmos/tools/tlm_viewer/screen'

module Cosmos
  class OnloadWidget < Qt::Widget
    include Widget

    def initialize(parent_layout = nil, string_to_eval)
      super(parent_layout)
      #self.text = 'this is the dumb text'.to_s.remove_quotes
      parent_layout.addWidget(self) if parent_layout
      #puts self.screen.class.name
      puts (@screen == nil).to_s
	  #puts (self.methods - Object.methods).to_s
      #parent_layout.addWidget(self) if parent_layout
      @string_to_eval = string_to_eval
      @evaluated = false
	  puts "from onload widget initializer"
	  eval(@string_to_eval)
	  a_screen = Cosmos::Screen.new()
    end
  end
end