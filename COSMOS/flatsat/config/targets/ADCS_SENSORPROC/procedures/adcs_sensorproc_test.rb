# To add this test to Test Runner edit config/tools/test_runner/test_runner.txt
# Add this line:
#   REQUIRE_UTILITY 'adcs_sensorproc_test'
#
# Test Runner test script
class Adcs_sensorprocTest < Cosmos::Test
  # def setup
  #   # Implement group level setup
  # end

  def test_command
    cmd("ADCS_SENSORPROC COMMAND")
    wait_check("ADCS_SENSORPROC STATUS BOOL == 'FALSE'", 5)
  end

  # def teardown
  #   # Implement group level teardown
  # end
end

class Adcs_sensorprocSuite < Cosmos::TestSuite
  # def setup
  #   # Implement suite level setup
  # end

  def initialize
    super()
    add_test('Adcs_sensorprocTest')
  end

  # def teardown
  #   # Implement suite level teardown
  # end
end
