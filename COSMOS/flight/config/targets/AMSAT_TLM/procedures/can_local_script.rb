# Script Runner test script
cmd("PEAK_CAN COMMAND")
wait_check("PEAK_CAN STATUS BOOL == 'FALSE'", 5)
