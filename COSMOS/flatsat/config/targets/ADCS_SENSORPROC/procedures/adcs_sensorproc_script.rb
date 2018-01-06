# Script Runner test script
cmd("ADCS_SENSORPROC COMMAND")
wait_check("ADCS_SENSORPROC STATUS BOOL == 'FALSE'", 5)
