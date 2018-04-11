# To add this test to Test Runner edit config/tools/test_runner/test_runner.txt
# Add this line:
#   REQUIRE_UTILITY 'adcs_sensorproc_test'

class GPSBootTest < Cosmos::Test
  def setup
  
  end
  
  def test
    cmd("ADCS_SENSORPROC GPS_ENABLE with ENABLE 1")
    wait_check("ADCS_SENSORPROC GPSPOWER STATE == 'ON'", 20) # wait for ON state
    cmd("ADCS_SENSORPROC GPS_ENABLE with ENABLE 0")
    wait_check("ADCS_SENSORPROC GPSPOWER STATE == 'OFF'", 5) # wait for OFF state
  end
  
  def teardown
  
  end
end

class Adcs_sensorprocSuite < Cosmos::TestSuite
  # def setup
  #   # Implement suite level setup
  # end

  def initialize
    super()
    add_test('GPSBootTest')
  end

  # def teardown
  #   # Implement suite level teardown
  # end
end
