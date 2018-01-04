# Script Runner test script
cmd("EPS_GEN COMMAND")
wait_check("EPS_GEN STATUS BOOL == 'FALSE'", 5)
