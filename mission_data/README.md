# Data from the HuskySat-1 Mission
## Mission Details
HuskySat-1 (HS-1) was the first satellite mission launched by the University of Washington.  It is also the first student-built satellite to be launched in the state of Washington.  The purpose of the 3U+ cubesat was to evaluate experimental communication and electric propulsion technology as well as increase the space presence of the university.  HS-1 was launched on Northrup Grumman's NG-12 on November 2, 2019 and deployed from the Cygnus craft on January 31, 2020.  The university's 90-day mission concluded on May 1, 2020, at which point ownership of the craft was transferred to the AMSAT corporation for use as an amateur radio transponder.

More mission details here: https://sites.google.com/prod/uw.edu/huskysatellitelab/huskysat-1

## Timestamps
Each data element is associated with a field called "time".  That field is the time that the data was recorded, as a [unix epoch](https://en.wikipedia.org/wiki/Unix_time) timestamp.  For reference, 0 is Jan 1, 1970 and the earliest recorded time on the mission is 1580512006, which is January 31, 2020, 23:06:46 (UTC)

## Power Domains
Most systems on HS-1 were enabled and disabled in separate power domains to conserve power and mitigate the effects of partial failure.  Telemetry was not collected for each system when it was unpowered.  The allocation is as follows:

System | Power Domain | Description
--- | --- | ---
COM2 | COM2 | 24 GHz Radio
RAHS | RAHS | Camera
BDOT | BDOT | ADCS controler
MTQ | BDOT | Magnetorquer controller
GEN | EPS | Power generation
BATT | EPS | Battery management
ESTIM | ESTIM | Position estimator
MPC | ESTIM | Model predictive controller
SENSORPROC | ESTIM | Sensor input and processing
PPT | PPT | Thruster

The primary communications system (COM1) and the power distribution board (DIST) were always enabled.  The COM2 and RAHS domains had comparatively large power requirements, and as such were automatically disabled twelve minutes after power-on.  All other domains are enabled and disabled by command, except for automatic disables in the case of over-current (domain specific) and under-voltage (full spacecraft) events.

## Transmission Modes
The COM1 systems had several communication modes, each of which selectively sends down certain telemetry items based on their classification.  For a full list of packets by classification and classifications per mode, see [transmission_mode](https://github.com/UWCubeSat/DS1Ops/tree/master/mission_data/transmission_mode).

## Data Aggregates
Due to limited storage and downlink, data were often aggregated and only statistics pertaining to each aggregate were collected.  If a field represents one of these statistics, its name will be the aggregate name followed by `_MIN`, `_MAX`, `_AVG`, or sometimes `_VAR` or `_Variance` for variance.

Minimums and maximums were all-time extremes, though they were reset by command several times.  Note here that the command to reset minimumns and maximums only affected the systems that were powered at the time it was received by HS-1.

Average and variance readings give a view of the data that is closer to instananeous, as they represent the average or variance of the data over approximately the previous 64 seconds.
