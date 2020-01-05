require 'cosmos/tools/tlm_viewer/widgets/timegraph_widget'

module Cosmos
  class BettergraphWidget < TimegraphWidget
    include Widget

    def initialize(parent_layout, target_name, packet_name, item_name, graph_title, num_samples = 100, width = 300, height = 200, point_size = 5, time_item_name = 'PACKET_TIMESECONDS', value_type = :CONVERTED)
      super(parent_layout, target_name, packet_name, item_name, num_samples, width, height, point_size, time_item_name, value_type)
      self.title = graph_title
    end
  end
end