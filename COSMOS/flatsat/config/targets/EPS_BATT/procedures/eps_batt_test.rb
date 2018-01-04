# To add this test to Test Runner edit config/tools/test_runner/test_runner.txt
# Add this line:
#   REQUIRE_UTILITY 'eps_batt_test'
#
# Test Runner test script
class Eps_battTest < Cosmos::Test
  # def setup
  #   # Implement group level setup
  # end

  def test_command
    cmd("EPS_BATT COMMAND")
    wait_check("EPS_BATT STATUS BOOL == 'FALSE'", 5)
  end

  # def teardown
  #   # Implement group level teardown
  # end
end

class Eps_battSuite < Cosmos::TestSuite
  # def setup
  #   # Implement suite level setup
  # end

  def initialize
    super()
    add_test('Eps_battTest')
  end

  # def teardown
  #   # Implement suite level teardown
  # end
end
