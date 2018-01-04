# Script Runner test script
cmd("EPS_BATT COMMAND")
wait_check("EPS_BATT STATUS BOOL == 'FALSE'", 5)
