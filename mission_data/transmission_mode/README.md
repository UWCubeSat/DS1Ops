# Transmission Mode
The COM1 radio had four unique transmission modes, each of which caused different classes of telemetry items to be downlinked at different rates.  An outline of the operating modes and packet classifications follows.

## Mode Descriptions

### Safe Mode
Safe Mode was a low-power operating mode.  Essential telemetry was transmitted, but at a low rate.

### Health Mode
This was the default operating mode of the COM1 system and as such was the transmission mode an overwhelming majority of the time.

### Real-Time Mode
Sometimes called "Science Mode", Real-Time mode is a temporary mode that was commanded each time by our Seattle ground station.  After a short amount of time, usually 15 minutes, the COM1 system reverted back to the previous mode, usually Health.

### Camera Mode
Like Real-Time, Camera Mode is a temporary commanded mode.  During the time COM1 was in Camera Mode, only WOD and picture data were downlinked.

## Whole-Orbit Data
Unlike other packet classifications, Whole-Orbit Data (WOD) packets were stored in an approximately 90-minute long circular buffer and continually retransmitted.  Unfortunatly, the WOD system failed on February 12, 2020.

## Telemetry by Mode

| Mode | Classes Transmitted |
| --- | --- |
| Safe | WOD, Health |
| Health | WOD, Health |
| Real-Time | WOD, Health, Real-Time |
| Camera | WOD, Camera |

## Packet Classifications

| WOD | Health | Real-Time | Camera |
| --- | --- | --- | --- |
| BATT_1 | BATT_H1 | BATT_1 | RAHS_CAMERA |
| COM1_MODE | BATT_H2 | BATT_4 ||
| DIST_1 | BATT_2 | BATT_7 ||
| GEN_10 | BATT_3 | BDOT_1 ||
|| BATT_5 | BODT_2 ||
|| BATT_6 | BDOT_3 ||
|| BDOT_H1 | BDOT_4 ||
|| BDOT_H2 | BDOT_5 ||
|| BDOT_7 | BDOT_6 ||
|| BDOT_8 | CMD_MTQ_BDOT ||
|| BDOT_9 | DIST_2 ||
|| BDOT_10 | DIST_3 ||
|| BDOT_11 | DIST_5 ||
|| DIST_H1 | DIST_6 ||
|| DIST_H2 | DIST_7 ||
|| DIST_4 | DIST_8 ||
|| GEN_H1 | DIST_9 ||
|| GEN_H2 | DIST_10 ||
|| MPC_H1 | DIST_11 ||
|| MPC_H2 | DIST_12 ||
|| MTQ_H1 | DIST_13 ||
|| MTQ_H2 | DIST_14 ||
|| MTQ_2 | DIST_15 ||
|| MTQ_3 | DIST_16 ||
|| MTQ_4 | DIST_17 ||
|| MTQ_5 | DIST_18 ||
|| PPT_H1 | ESTIM_H1 ||
|| PPT_H2 | ESTIM_H2 ||
|| SP_H1 | ESTIM_2 ||
||| ESTIM_3 ||
||| ESTIM_4 ||
||| ESTIM_5 ||
||| ESTIM_6 ||
||| ESTIM_7 ||
||| ESTIM_8 ||
||| ESTIM_9 ||
||| ESTIM_10 ||
||| ESTIM_11 ||
||| ESTIM_12 ||
||| ESTIM_13 ||
||| ESTIM_14 ||
||| GEN_1 ||
||| GEN_2 ||
||| GEN_3 ||
||| GEN_4 ||
||| GEN_5 ||
||| GEN_6 ||
||| GEN_7 ||
||| GEN_8 ||
||| GEN_9 ||
||| MPC_2 ||
||| MPC_3 ||
||| MPC_4 ||
||| MPC_5 ||
||| MPC_6 ||
||| MPC_7 ||
||| MPC_8 ||
||| MPC_9 ||
||| MPC_10 ||
||| MPC_11 ||
||| MPC_15 ||
||| MTQ_ACK ||
||| PPT_1 ||
||| PPT_2 ||
||| SP_2 ||
||| SP_3 ||
||| SP_4 ||
||| SP_5 ||
||| SP_6 ||
||| SP_7 ||
||| SP_8 ||
||| SP_9 ||
||| SP_10 ||
||| SP_11 ||
||| SP_12 ||
||| SP_13 ||
||| SP_14 ||
||| SP_15 ||
||| SP_16 ||
||| SP_17 ||
