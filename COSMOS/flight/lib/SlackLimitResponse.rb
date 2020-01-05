require 'cosmos/packets/limits_response'
require 'net/http'
require 'net/https'
require 'uri'
require 'json'


class Slacklimitresponse < Cosmos::LimitsResponse
  def call(packet, item, old_limits_state)
    #testing
    uri = URI.parse("https://hooks.slack.com/services/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")
	#real
	#uri = URI.parse("https://hooks.slack.com/services/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")
    header = {'Content-Type': 'application/json'}
	packet_name = packet.packet_name
	item_name = item.name.dup
	if item_name.include? packet_name
		item_name.slice! packet_name+"_"
	end
    case item.limits.state
    when :RED_HIGH
      body = { text: 'Warning `'+packet_name+' '+item_name+"` is the high red zone",
	  attachments:[
	  color:"#ff0000",
	  text:"#{tlm(packet.target_name+' '+packet.packet_name+' '+item.name).round(3)} "+item.units] }
    when :RED_LOW
      body = { text: 'Warning `'+packet_name+' '+item_name+"` is the low red zone",
	  attachments:[
	  color:"#ff0000",
	  text:"#{tlm(packet.target_name+' '+packet.packet_name+' '+item.name).round(3)} "+item.units] }
    when :YELLO_HIGH
      body = { text: 'Warning `'+packet_name+' '+item_name+"` is the high yellow zone",
	  attachments:[
	  color:"#fcce00",
	  text:"#{tlm(packet.target_name+' '+packet.packet_name+' '+item.name).round(3)} "+item.units] }
    when :YELLOW_LOW
      body = { text: 'Warning `'+packet_name+' '+item_name+"` is the low yellow zone",
	  attachments:[
	  color:"#fcce00",
	  text:"#{tlm(packet.target_name+' '+packet.packet_name+' '+item.name).round(3)} "+item.units] }
    end
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Post.new(uri.request_uri, header)
    request.body = body.to_json

    http.request(request)
  end
end