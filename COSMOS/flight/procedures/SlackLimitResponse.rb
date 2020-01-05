require 'cosmos/packets/limits_response'
require 'net/http'
require 'net/https'
require 'uri'
require 'json'


class Slacklimitresponse < Cosmos::LimitsResponse
  def call(packet, item, old_limits_state)
    uri = URI.parse("https://hooks.slack.com/services/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")
    header = {'Content-Type': 'application/json'}
    case item.limits.state
    when :RED_HIGH
      body = { text: 'Warning lmit is in the high red zone' }
    when :RED_LOW
      body = { text: 'Warning lmit is in the low red zone' }
    when :YELLO_HIGH
      body = { text: 'Warning lmit is in the high yellow zone' }
    when :YELLOW_LOW
      body = { text: 'Warning lmit is in the low yellow zone' }
    end
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Post.new(uri.request_uri, header)
    request.body = body.to_json

    http.request(request)
  end
end