#!/usr/bin/env python3

# Copyright (c) 2013, Eduard Broecker
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that
# the following conditions are met:
#
#    Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

from __future__ import print_function
from __future__ import absolute_import

# from .log import setup_logger, set_log_level
#logger = setup_logger('root')
import sys
import os
sys.path.append('..')
import canmatrix.formats
import canmatrix.canmatrix as cm
import canmatrix.copy as cmcp

temperatureLimits=[15, 20, 30, 35]
signalToLimits = {
		"rc_eps_batt_h1_temp_avg":temperatureLimits,
	"rc_eps_batt_3_batt_temp_avg":temperatureLimits,
	"rc_adcs_bdot_h1_temp_avg":temperatureLimits,
	"rc_ppt_h1_temp_avg":temperatureLimits,
	"rc_eps_dist_h1_temp_avg":temperatureLimits,
	"rc_eps_gen_h1_temp_avg":temperatureLimits,
	"rc_adcs_estim_h1_temp_avg":temperatureLimits,
	"rc_adcs_mpc_h1_temp_avg":temperatureLimits,
	"rc_adcs_sp_h1_temp_avg":temperatureLimits,
	"rc_adcs_mtq_h1_temp_avg":temperatureLimits,
	"rc_com1_h1_temp_avg":temperatureLimits,
	"rc_com2_h1_temp_avg":temperatureLimits,
		
		"rc_eps_batt_h1_temp_max":temperatureLimits,
	"rc_adcs_bdot_h1_temp_max":temperatureLimits,
	"rc_ppt_h1_temp_max":temperatureLimits,
	"rc_eps_dist_h1_temp_max":temperatureLimits,
	"rc_eps_gen_h1_temp_max":temperatureLimits,
	"rc_adcs_estim_h1_temp_max":temperatureLimits,
	"rc_adcs_mpc_h1_temp_max":temperatureLimits,
	"rc_adcs_sp_h1_temp_max":temperatureLimits,
	"rc_adcs_mtq_h1_temp_max":temperatureLimits,
	"rc_com1_h1_temp_max":temperatureLimits,
	"rc_com2_h1_temp_max":temperatureLimits,
		
		"rc_eps_batt_h1_temp_min":temperatureLimits,
	"rc_adcs_bdot_h1_temp_min":temperatureLimits,
	"rc_ppt_h1_temp_min":temperatureLimits,
	"rc_eps_dist_h1_temp_min":temperatureLimits,
	"rc_eps_gen_h1_temp_min":temperatureLimits,
	"rc_adcs_estim_h1_temp_min":temperatureLimits,
	"rc_adcs_mpc_h1_temp_min":temperatureLimits,
	"rc_adcs_sp_h1_temp_min":temperatureLimits,
	"rc_adcs_mtq_h1_temp_min":temperatureLimits,
	"rc_com1_h1_temp_min":temperatureLimits,
	"rc_com2_h1_temp_min":temperatureLimits,
	
	"rc_eps_dist_3_batt_v_avg":[5.2, 5.8,7.3, 7.7],
	"rc_eps_dist_4_com1_c_avg":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_5_com1_v_avg":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_6_com2_c_avg":[0.07, 0.095, 0.135, 0.20],
	"rc_eps_dist_7_com2_v_avg":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_8_rahs_c_avg":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_9_rahs_v_avg":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_10_bdot_c_avg":[0.01,0.08,0.12,0.15],
	"rc_eps_dist_11_bdot_v_avg":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_12_estim_c_avg":[0.01,0.08,0.12,0.15],
	"rc_eps_dist_13_estim_v_avg":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_14_eps_c_avg":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_15_eps_v_avg":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_16_ppt_c_avg":[0.1,0.25,0.4,0.5],
	"rc_eps_dist_17_ppt_v_avg":[0.5,3.0,7.0,10.0],
	
	"rc_eps_dist_3_batt_v_min":[5.2, 5.8,7.3, 7.7],
	"rc_eps_dist_4_com1_c_min":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_5_com1_v_min":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_6_com2_c_min":[0.07, 0.095, 0.135, 0.20],
	"rc_eps_dist_7_com2_v_min":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_8_rahs_c_min":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_9_rahs_v_min":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_10_bdot_c_min":[0.01,0.08,0.12,0.15],
	"rc_eps_dist_11_bdot_v_min":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_12_estim_c_min":[0.01,0.08,0.12,0.15],
	"rc_eps_dist_13_estim_v_min":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_14_eps_c_min":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_15_eps_v_min":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_16_ppt_c_min":[0.1,0.25,0.4,0.5],
	"rc_eps_dist_17_ppt_v_min":[0.5,3.0,7.0,10.0],
	
	"rc_eps_dist_3_batt_v_max":[5.2, 5.8,7.3, 7.7],
	"rc_eps_dist_4_com1_c_max":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_5_com1_v_max":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_6_com2_c_max":[0.07, 0.095, 0.135, 0.20],
	"rc_eps_dist_7_com2_v_max":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_8_rahs_c_max":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_9_rahs_v_max":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_10_bdot_c_max":[0.01,0.08,0.12,0.15],
	"rc_eps_dist_11_bdot_v_max":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_12_estim_c_max":[0.01,0.08,0.12,0.15],
	"rc_eps_dist_13_estim_v_max":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_14_eps_c_max":[0.01, 0.08, 0.12, 0.15],
	"rc_eps_dist_15_eps_v_max":[0.5,3.0,7.0,10.0],
	"rc_eps_dist_16_ppt_c_max":[0.1,0.25,0.4,0.5],
	"rc_eps_dist_17_ppt_v_max":[0.5,3.0,7.0,10.0],
	
	"rc_eps_gen_2_pnl_1_voltage_avg":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_3_pnl_2_voltage_avg":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_4_pnl_3_voltage_avg":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_4_pnl_1_current_avg":[0.003,.05,.3,.4],
	"rc_eps_gen_5_pnl_2_current_avg":[0.003,.05,.45,.6],
	"rc_eps_gen_6_pnl_3_current_avg":[0.003,.05,.3,.4],
	"rc_eps_gen_7_pnl_1_power_avg":[0.06,1.0,3.0,4.0],
	"rc_eps_gen_7_pnl_2_power_avg":[0.06,1.0,6.0,7.0],
	"rc_eps_gen_8_pnl_3_power_avg":[0.06,1.0,3.0,4.0],
	"rc_eps_gen_9_pnl_1_temp_avg":[17,19.5,23,25],
	"rc_eps_gen_9_pnl_2_temp_avg":[17,19.5,23,25],
	"rc_eps_gen_9_pnl_3_temp_avg":[17,19.5,23,25],
	
	"rc_eps_gen_2_pnl_1_voltage_min":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_2_pnl_2_voltage_min":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_3_pnl_3_voltage_min":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_4_pnl_1_current_min":[0.003,.05,.3,.4],
	"rc_eps_gen_5_pnl_2_current_min":[0.003,.05,.45,.6],
	"rc_eps_gen_5_pnl_3_current_min":[0.003,.05,.3,.4],
	"rc_eps_gen_6_pnl_1_power_min":[0.06,1.0,3.0,4.0],
	"rc_eps_gen_7_pnl_2_power_min":[0.06,1.0,6.0,7.0],
	"rc_eps_gen_8_pnl_3_power_min":[0.06,1.0,3.0,4.0],
	"rc_eps_gen_8_pnl_1_temp_min":[17,19.5,23,25],
	"rc_eps_gen_9_pnl_2_temp_min":[17,19.5,23,25],
	"rc_eps_gen_9_pnl_3_temp_min":[17,19.5,23,25],
	
	"rc_eps_gen_2_pnl_1_voltage_max":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_3_pnl_2_voltage_max":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_3_pnl_3_voltage_max":[3.0, 9.0,17.0,18.0],
	"rc_eps_gen_4_pnl_1_current_max":[0.003,.05,.3,.4],
	"rc_eps_gen_5_pnl_2_current_max":[0.003,.05,.45,.6],
	"rc_eps_gen_6_pnl_3_current_max":[0.003,.05,.3,.4],
	"rc_eps_gen_6_pnl_1_power_max":[0.06,1.0,3.0,4.0],
	"rc_eps_gen_7_pnl_2_power_max":[0.06,1.0,6.0,7.0],
	"rc_eps_gen_8_pnl_3_power_max":[0.06,1.0,3.0,4.0],
	"rc_eps_gen_9_pnl_1_temp_max":[17,19.5,23,25],
	"rc_eps_gen_9_pnl_2_temp_max":[17,19.5,23,25],
	"rc_eps_gen_9_pnl_3_temp_max":[17,19.5,23,25],

	"rc_eps_batt_4_voltage_avg":[5.2, 5.8, 7.3, 7.7],
	"rc_eps_batt_3_current_avg":[-10.0, -8.0, 4.5, 6.0],
	"rc_eps_batt_2_node_v_avg":[2.6, 2.9, 3.65, 3.85],
	"rc_eps_batt_5_node_c_avg":[-10.0, -8.0, 4.5, 6.0]
}
signalConversions = {
	"1/73 nT":"value * 73.0",
	"dK":"(55.0*(value-1255.0))/214.0 +30.0",
	"dk":"(55.0*(value-1255.0))/214.0 +30.0",
	"2^-15 seconds":"value * 2.0**-15",
	"mW":"value * 0.001",
	"mA":"value * 0.001",
	"dmA":"value * 0.0001",
	"mV":"value * 0.001",
	"cA":"value * 0.01",
	"2^-8 seconds":"value * 2.0**-8",
	"2^-15s":"value * 2.0**-15",
	"dmA (0.1mA)":"value * 0.0001",
	"2^-8s":"value * 2.0**-8",
	"2^-8 s":"value >> 8",
	"1/73 nanoTeslas":"value * 1.0/73",
	"73 nanoTeslas":"value * 73",
	"0.004375 deg/s":"value * 0.004375",
	"60/32767 degrees":"value * 60.0/32767",
	"1/32768 units":"value * 3.051757e-5",
	"raw node voltage":"value * 0.004",
	"raw current batt":"(value - 32767) / 3276.7",
	"raw voltage":"23.6 * value / 65535",
	"raw node current batt":"value / 327.68",
	"cC":"value / 100.0",
	"raw node current dist":"value / 2048.0",
	"raw dist battery voltage":"7.21698125 * value / 4096",
	"raw node current gen":"value * 1.5 / 32768",
	"raw power gen":"value * 3 / 3276.8",
	"raw tmp36":"value - 50",
    "ocpThresh":"value / 20.0",
	"bdot gain":"value / 100.0"
}
signalUnits = {
	"1/73 nT":"nanoTeslas nT",
	"dK":"Celcius C",
	"dk":"Celcius C",
	"2^-15 seconds":"Seconds s",
	"mW":"Watts W",
	"mA":"Amps A",
	"dmA":"Amps A",
	"mV":"Volts V",
	"cA":"Amps A",
	"2^-8 seconds":"Seconds s",
	"2^-15s":"Seconds s",
	"dmA (0.1mA)":"Amps A",
	"2^-8s":"Seconds s",
	"2^-8 s":"Seconds s",
	"r/s":"Radians_Per_Second r/s",
	"m/s":"Meters_Per_Second m/s",
	"m":"Meters m",
	"1/73 nanoTeslas":"Nanoteslas nT",
	"73 nanoTeslas":"nanoTeslas nT",
	"0.004375 deg/s":"Degrees_Per_Second deg/s",
	"60/32767 degrees":"Degrees deg",
	"C":"Degrees_Celcius C",
	"deg C":"Degrees_Celcius C",
	"Deg C":"Degrees_Celcius C",
	"s":"Seconds s",
	"1/32768 units":"Units u",
	"raw node voltage":"Volts V",
	"raw current batt":"Amps A",
	"raw voltage":"Volts V",
	"raw node current batt":"Amps A",
        "cC":"Degrees_Celcius C",
	"raw node current dist":"Amps A",
	"raw dist battery voltage":"Volts V",
	"raw node current gen":"Amps A",
	"raw power gen":"Watts W",
	"raw tmp36":"Degrees_Celcius C",
    "ocpThresh":"Amps A",
	"minutes":"Minutes min"
}

# adds a FORMAT_STRING to the signal depending on what unit was used
unitFormat = {
	"m/s":"%0.4f",
	"m":"%0.1f",
	"u":"%0.4f",
	"1/32768 units":"%0.4f",
	"deg":"%0.4f",
	"0.004375 deg/s":"%0.2f",
	"d":"%0.4f",
	"s":"%0.4f",
	"C":"%0.3f",
	"dK":"%0.3f",
	"dk":"%0.3f",
	"r/s":"%0.3f"
        
}

enumToColor = { #these can be green, yellow, or red
	"on":"GREEN",
	"off_manual":"YELLOW",
	"off_overcurrent":"RED",
	"off_batt_undervoltage":"RED",
	"off_initial":"YELLOW",
	"off_autoshutoff":"RED",
	"unknown":"RED",
	"ENABLED":"GREEN",
	"DISABLED":"RED",
	"CHARGING":"GREEN",
	"NOTCHARGING":"YELLOW"
}

frameToDerivedValues = {
	"rc_eps_batt_7":["acc_charge_min", "acc_charge_avg", "acc_charge_max", "rc_eps_batt_7_voltage_diff"]
}

derivedValueToConversion = {
	"acc_charge_min":"packet.read('RC_EPS_BATT_7_ACC_CHARGE_MIN') * 2 ** (2 * ((System.telemetry.value(\"{}\", \"RC_EPS_BATT_6\", \"RC_EPS_BATT_6_CTRL\") & 0b00111000) >> 3)) * 17 / 24576",
	"acc_charge_avg":"packet.read('RC_EPS_BATT_7_ACC_CHARGE_AVG') * 2 ** (2 * ((System.telemetry.value(\"{}\", \"RC_EPS_BATT_6\", \"RC_EPS_BATT_6_CTRL\") & 0b00111000) >> 3)) * 17 / 24576",
	"acc_charge_max":"packet.read('RC_EPS_BATT_7_ACC_CHARGE_MAX') * 2 ** (2 * ((System.telemetry.value(\"{}\", \"RC_EPS_BATT_6\", \"RC_EPS_BATT_6_CTRL\") & 0b00111000) >> 3)) * 17 / 24576",
	"rc_eps_batt_7_voltage_diff":"(1000 * System.telemetry.value(\"{}\", \"RC_EPS_BATT_4\", \"RC_EPS_BATT_4_VOLTAGE_AVG\") - (2 * System.telemetry.value(\"{}\", \"RC_EPS_BATT_2\", \"RC_EPS_BATT_2_NODE_V_AVG\")))"
}

derivedValueToUnits = {
	"acc_charge_min":"milliAmpH mAH",
	"acc_charge_avg":"milliAmpH mAH",
	"acc_charge_max":"milliAmpH mAH",
	"rc_eps_batt_7_voltage_diff":"milliVolts mV"
}

# adds a FORMAT_STRING for specific signals. Overrides the unit formatting
signalFormat = {
  "rc_adcs_estim_8_epoch":"%.0f",
  "rc_eps_batt_2_node_v_min":"%.4f",
  "rc_eps_batt_2_node_v_max":"%.4f",
  "rc_eps_batt_2_node_v_avg":"%.4f",

  "rc_eps_batt_5_node_c_min":"%.4f",
  "rc_eps_batt_5_node_c_max":"%.4f",
  "rc_eps_batt_5_node_c_avg":"%.4f",

  "rc_eps_batt_4_voltage_min":"%.4f",
  "rc_eps_batt_4_voltage_max":"%.4f",
  "rc_eps_batt_4_voltage_avg":"%.4f",

  "rc_eps_batt_3_current_min":"%.4f",
  "rc_eps_batt_3_current_max":"%.4f",
  "rc_eps_batt_3_current_avg":"%.4f",

  "rc_eps_batt_7_voltage_diff":"%.4f"
}

signalsWithOverflow=[
	"cmd_rollcall_met",
	"grnd_epoch_val",
	"rc_eps_dist_2_met",
	"rc_adcs_estim_8_epoch"
]
overFlowSignals=[
	"cmd_rollcall_met_overflow",
	"grnd_epoch_val_overflow",
	"rc_eps_dist_2_met_overflow",
	"rc_adcs_estim_8_epoch_overflow"
]
def toPyObject(infile, **options):
	dbs = {}

	#logger.info("Importing " + infile + " ... ")
	dbs = canmatrix.formats.loadp(infile, **options)
	#logger.info("done\n")

	#logger.info("Exporting " + outfileName + " ... ")

	outdbs = {}
	for name in dbs:
		db = None

		if 'ecus' in options and options['ecus'] is not None:
			ecuList = options['ecus'].split(',')
			db = cm.CanMatrix()
			for ecu in ecuList:
				#logger.info("Copying ECU " + ecu)
				cmcp.copyBUwithFrames(ecu, dbs[name], db)
		if 'frames' in options and options['frames'] is not None:
			frameList = options['frames'].split(',')
			db = cm.CanMatrix()
			for frame in frameList:
				#logger.info("Copying Frame " + frame)
				cmcp.copyFrame(frame, dbs[name], db)
		if db is None:
			db = dbs[name]

		if 'merge' in options and options['merge'] is not None:
			mergeFiles = options['merge'].split(',')
			for database in mergeFiles:
				mergeString = database.split(':')
				dbTempList = canmatrix.formats.loadp(mergeString[0])
				for dbTemp in dbTempList:
					if mergeString.__len__() == 1:
						print ("merge complete: " + mergeString[0])
						for frame in dbTempList[dbTemp].frames:
							cmcp.copyFrame(frame.id, dbTempList[dbTemp], db)
					for mergeOpt in mergeString[1:]:
						if mergeOpt.split('=')[0] == "ecu":
							cmcp.copyBUwithFrames(
								mergeOpt.split('=')[1], dbTempList[dbTemp], db)
						if mergeOpt.split('=')[0] == "frame":
							cmcp.copyFrame(
								mergeOpt.split('=')[1], dbTempList[dbTemp], db)

		if 'renameEcu' in options and options['renameEcu'] is not None:
			renameTuples = options['renameEcu'].split(',')
			for renameTuple in renameTuples:
				old, new = renameTuple.split(':')
				db.renameEcu(old, new)
		if 'deleteEcu' in options and options['deleteEcu'] is not None:
			deleteEcuList = options['deleteEcu'].split(',')
			for ecu in deleteEcuList:
				db.delEcu(ecu)
		if 'renameFrame' in options and options['renameFrame'] is not None:
			renameTuples = options['renameFrame'].split(',')
			for renameTuple in renameTuples:
				old, new = renameTuple.split(':')
				db.renameFrame(old, new)
		if 'deleteFrame' in options and options['deleteFrame'] is not None:
			deleteFrameList = options['deleteFrame'].split(',')
			for frame in deleteFrameList:
				db.delFrame(frame)
		if 'renameSignal' in options and options['renameSignal'] is not None:
			renameTuples = options['renameSignal'].split(',')
			for renameTuple in renameTuples:
				old, new = renameTuple.split(':')
				db.renameSignal(old, new)
		if 'deleteSignal' in options and options['deleteSignal'] is not None:
			deleteSignalList = options['deleteSignal'].split(',')
			for signal in deleteSignalList:
				db.delSignal(signal)

		if 'deleteZeroSignals' in options and options['deleteZeroSignals']:
			db.deleteZeroSignals()

		if 'deleteSignalAttributes' in options and options[
				'deleteSignalAttributes']:
			unwantedAttributes = options['deleteSignalAttributes'].split(',')
			db.delSignalAttributes(unwantedAttributes)

		if 'deleteFrameAttributes' in options and options[
				'deleteFrameAttributes']:
			unwantedAttributes = options['deleteFrameAttributes'].split(',')
			db.delFrameAttributes(unwantedAttributes)

		if 'deleteObsoleteDefines' in options and options[
				'deleteObsoleteDefines']:
			db.deleteObsoleteDefines()

		if 'recalcDLC' in options and options['recalcDLC']:
			db.recalcDLC(options['recalcDLC'])

		#logger.info(name)
		#logger.info("%d Frames found" % (db.frames.__len__()))

		outdbs[name] = db

	#print(outdbs[''].frames._list[0]._name)
	return outdbs['']
'''
def createCHeader(candb, cFileName):
	#print(candb.frames._list[0]._name)
	cFile = open(cFileName, "w")
	cFile.write("#ifndef CANDB_HEADER\n#define CANDB_HEADER\n\n")
	cFile.write("#include <stdint.h>\n\n")
	for frame in candb.frames:
		cFile.write("typedef struct {\n")
		for sig in frame:
			if sig.is_signed:
				cFile.write("\tint")
			else:
				cFile.write("\tuint")
			if sig.signalsize == 8:
				cFile.write("8_t ")
			elif sig.signalsize == 16:
				cFile.write("16_t ")
			elif sig.signalsize == 32:
				cFile.write("32_t ")
			else:
				cFile.write("64_t ")
			cFile.write(sig.name + ";\n")
		cFile.write("} " + frame.name + ";\n\n")
	cFile.write("\n#endif")
	cFile.close()'''

def tlmGetType(signal):
	if (signal.is_float):
		return "FLOAT"
	elif (signal.is_signed):
		return "INT"
	else:
		return "UINT"

def createCosmosTlm(candb, tlmFileName):
	tlmFile = open(tlmFileName, "w")
	tlm_id = 0;
	interfaceName = tlmFileName[:-8] #grabs the filename minus _tlm.txt
	for frame in candb.frames:
		tlmFile.write("TELEMETRY {}_TLM {} BIG_ENDIAN \n".format(interfaceName, frame.name))
		tlmFile.write("\tAPPEND_ITEM LENGTH 16 UINT \"Length of TCP-ized CAN message (always 36/0x24 bytes) \" \n ")
		tlmFile.write("\tAPPEND_ID_ITEM FIXED_TYPE 16 UINT 128 \"Fixed message type for CAN\" BIG_ENDIAN\n")
		tlmFile.write("\tAPPEND_ITEM TAG 64 UINT \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
		tlmFile.write("\tAPPEND_ITEM TIMESTAMP_L 32 UINT \"Timestamp of the CAN message, in microseconds.  This is the lower 4 bytes of the timestamp.\"\n")
		tlmFile.write("\tAPPEND_ITEM TIMESTAMP_H 32 UINT \"Timestamp of the CAN message, in microseconds.  This is the upper 4 bytes of the timestamp.\"\n")
		tlmFile.write("\tAPPEND_ITEM CHANNEL 8 UINT \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
		tlmFile.write("\tAPPEND_ITEM DLC 8 UINT \"Date Length Count from the CAN message.\"\n")
		tlmFile.write("\tAPPEND_ITEM FLAGS 16 UINT \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
		tlmFile.write("\tAPPEND_ITEM CANID_PADDING 1 UINT \"Fixed value of 0 - reserved.\"\n")
		tlmFile.write("\tAPPEND_ITEM CANID_RTR 1 UINT \"RTR value.\"\n")
		tlmFile.write("\tAPPEND_ITEM CANID_TYPE 1 UINT \"Indicates whether the message is a standard or extended frame.\"\n")
		tlmFile.write("\tAPPEND_ID_ITEM CANID_ID 29 UINT {} \"The ID (normal or extended) portion of the 'CAN ID' set of headers.\"\n".format(frame.id))
		tlmFile.write("\t\tSTATE EXTENDED 1\n")
		tlmFile.write("\t\tSTATE STANDARD 0\n")
		signal_size = 0
		signalStrings = {}
		for signal in frame:
			tlmString=""
			signal_size = signal_size + signal.signalsize
			signalType = tlmGetType(signal)
			if signal.is_little_endian and False:
				signalEndian = "LITTLE_ENDIAN"
			else:
				signalEndian = "BIG_ENDIAN"
			if signal.name in signalsWithOverflow:
				tlmString += ("\tAPPEND_ITEM {} {} {} \"{}\" {}\n".format(signal.name,
															40,
															signalType,
															signal.comment,
															signalEndian))
			elif not (signal.name in overFlowSignals):
				tlmString +=("\tAPPEND_ITEM {} {} {} \"{}\" {}\n".format(signal.name,
															signal.signalsize,
															signalType,
															signal.comment,
															signalEndian))
			for key in sorted(signal._values.keys()):
				if signal._values[key] in enumToColor:
					tlmString +=("\t\tSTATE {} {} {}\n".format(signal._values[key].replace(" ", "_"),
															key,
															enumToColor[signal._values[key]]))
				else:
					tlmString +=("\t\tSTATE {} {}\n".format(signal._values[key].replace(" ", "_"),
															key))
			if signal.unit in signalUnits:
				tlmString +=("\t\tUNITS {}\n".format(signalUnits[signal.unit]))
			if signal.unit in signalConversions:
				tlmString +=("\t\tGENERIC_READ_CONVERSION_START\n")
				tlmString +=("\t\t\t"+ signalConversions[signal.unit] + "\n")
				tlmString +=("\t\tGENERIC_READ_CONVERSION_END\n")
			if signal.name in signalToLimits:
				tlmString +=("\t\tLIMITS DEFAULT 1 ENABLED {} {} {} {}\n".format(
															signalToLimits[signal.name][0],
															signalToLimits[signal.name][1],
															signalToLimits[signal.name][2],
															signalToLimits[signal.name][3]
															))
				tlmString +="\t\tLIMITS_RESPONSE SlackLimitResponse.rb\n"
                                
			if signal.name in signalFormat:
				tlmString += "\t\tFORMAT_STRING \"" + signalFormat[signal.name] + "\"\n"
			elif signal.unit in unitFormat:
				tlmString += "\t\tFORMAT_STRING \"" + unitFormat[signal.unit] + "\"\n"
			signalStrings[signal._startbit] = tlmString
		if signal_size != 64:
			signalStrings[64] = ("\tAPPEND_ITEM PADDING {} UINT \"Padded bits for CAN data\"\n".format(64 - signal_size))
		for i in sorted(signalStrings.keys()):
			tlmFile.write(signalStrings[i])
		if frame.name in frameToDerivedValues.keys():
			for derived in frameToDerivedValues[frame.name]:
				tlmFile.write("\tITEM {} 0 0 DERIVED\n".format(derived))
				if derived in derivedValueToUnits.keys():
					tlmFile.write("\t\tUNITS {}\n".format(derivedValueToUnits[derived]))
				if derived in derivedValueToConversion.keys():
					tlmFile.write("\t\tGENERIC_READ_CONVERSION_START\n\t\t\t{}\n\t\tGENERIC_READ_CONVERSION_END\n".format(derivedValueToConversion[derived].replace("{}", format(interfaceName))))
				if derived in signalFormat:
					tlmFile.write("\t\tFORMAT_STRING \"" + signalFormat[derived] + "\"\n")
				elif derived in unitFormat:
					tlmFile.write("\t\tFORMAT_STRING \"" + unitFormat[derived] + "\"\n")
		tlmFile.write("\n")
	tlmFile.write("""
TELEMETRY {}_TLM general_can_message BIG_ENDIAN 
	APPEND_ITEM LENGTH 16 UINT "Length of TCP-ized CAN message (always 36/0x24 bytes) " 
	APPEND_ID_ITEM FIXED_TYPE 16 UINT 128 "Fixed message type for CAN" BIG_ENDIAN
	APPEND_ITEM TAG 64 UINT "NOT USED in current PCAN-Ethernet Gateway DR hardware/software."
	APPEND_ITEM TIMESTAMP_L 32 UINT "Timestamp of the CAN message, in microseconds.  This is the lower 4 bytes of the timestamp."
	APPEND_ITEM TIMESTAMP_H 32 UINT "Timestamp of the CAN message, in microseconds.  This is the upper 4 bytes of the timestamp."
	APPEND_ITEM CHANNEL 8 UINT "NOT USED in current PCAN-Ethernet Gateway DR hardware/software."
	APPEND_ITEM DLC 8 UINT "Date Length Count from the CAN message."
	APPEND_ITEM FLAGS 16 UINT "NOT USED in current PCAN-Ethernet Gateway DR hardware/software."
	APPEND_ITEM CANID_PADDING 1 UINT "Fixed value of 0 - reserved."
	APPEND_ITEM CANID_RTR 1 UINT "RTR value."
	APPEND_ITEM CANID_TYPE 1 UINT "Indicates whether the message is a standard or extended frame."
	APPEND_ITEM CANID_ID 29 UINT "The ID (normal or extended) portion of the 'CAN ID' set of headers."
		STATE EXTENDED 1
		STATE STANDARD 0
	APPEND_ITEM DATA 64 UINT "CAN data"


	""".format(interfaceName))
def createCosmosCmd(candb, tlmFileName):
	tlmFile = open(tlmFileName, "w")
	tlm_id = 0;
	interfaceName = tlmFileName[:-8] #grabs the filename minus _cmd.txt
	for frame in candb.frames:
		tlmFile.write("COMMAND {}_CMD {} BIG_ENDIAN \n".format(interfaceName, frame.name))
		tlmFile.write("\tAPPEND_PARAMETER LENGTH 16 UINT MIN MAX  36 \"Length of TCP-ized CAN message (always 36/0x24 bytes) \" \n ")
		tlmFile.write("\t\tSTATE DEFAULT 36 \n")
		tlmFile.write("\tAPPEND_ID_PARAMETER FIXED_TYPE 16 UINT MIN MAX  128 \"Fixed message type for CAN\" BIG_ENDIAN\n")
		tlmFile.write("\t\tSTATE DEFAULT 128 \n")
		tlmFile.write("\tAPPEND_PARAMETER TAG 64 UINT MIN MAX  0 \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 0 \n")
		tlmFile.write("\tAPPEND_PARAMETER TIMESTAMP_L 32 UINT MIN MAX  0 \"Timestamp of the CAN message, in microseconds.  This is the lower 4 bytes of the timestamp.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 0 \n")
		tlmFile.write("\tAPPEND_PARAMETER TIMESTAMP_H 32 UINT MIN MAX  0 \"Timestamp of the CAN message, in microseconds.  This is the upper 4 bytes of the timestamp.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 0 \n")
		tlmFile.write("\tAPPEND_PARAMETER CHANNEL 8 UINT MIN MAX  0  \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 0 \n")
		tlmFile.write("\tAPPEND_PARAMETER DLC 8 UINT MIN MAX  8  \"Date Length Count from the CAN message.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 8 \n")
		tlmFile.write("\tAPPEND_PARAMETER FLAGS 16 UINT MIN MAX  2 \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 2 \n")
		tlmFile.write("\tAPPEND_PARAMETER CANID_PADDING 1 UINT MIN MAX  0 \"Fixed value of 0 - reserved.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 0 \n")
		tlmFile.write("\tAPPEND_PARAMETER CANID_RTR 1 UINT MIN MAX  0 \"RTR value.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 0 \n")
		tlmFile.write("\tAPPEND_PARAMETER CANID_TYPE 1 UINT MIN MAX  1  \"Indicates whether the message is a standard or extended frame.\"\n")
		tlmFile.write("\t\tSTATE DEFAULT 1 \n")
		tlmFile.write("\tAPPEND_PARAMETER CANID_ID 29 UINT MIN MAX  {} \"The ID (normal or extended) portion of the 'CAN ID' set of headers.\"\n".format(frame.id))
		tlmFile.write("\t\tSTATE DEFAULT {} \n".format(frame.id))
		signal_size = 0
		signalStrings = {}
		for signal in frame:
			tlmString = ""
			signal_size = signal_size + signal.signalsize
			signalType = tlmGetType(signal)
			if signal.is_little_endian and False:
				signalEndian = "LITTLE_ENDIAN"
			else:
				signalEndian = "BIG_ENDIAN"
			if signal.name in signalsWithOverflow:
				tlmString += ("\tAPPEND_PARAMETER {} {} {} MIN MAX  0 \"{}\" {}\n".format(signal.name,
															40,
															signalType,
															signal.comment,
															signalEndian))
			elif not (signal.name in overFlowSignals):
				int(signal.min)
				tlmString += ("\tAPPEND_PARAMETER {} {} {} {} {}  0 \"{}\" {}\n".format(signal.name,
															signal.signalsize,
															signalType,
															int(signal.min),
															int(signal.max),
															signal.comment,
															signalEndian))
			for key in sorted(signal._values.keys()):
				tlmString +=("\t\tSTATE {} {}\n".format(signal._values[key].replace(" ", "_"),
															key))
			signalStrings[signal._startbit] = tlmString
		if signal_size != 64:
			signalStrings[64] = ("\tAPPEND_PARAMETER PADDING {} UINT MIN MAX 0 \"Padded bits for CAN data\"\n\n".format(64 - signal_size))
		for i in sorted(signalStrings.keys()):
			tlmFile.write(signalStrings[i])
def main():
	from optparse import OptionParser

	usage = """
	%prog [options] import-file

	import-file: *.dbc|*.dbf|*.kcd|*.arxml|*.json|*.xls(x)|*.sym

	followig formats are availible at this installation:
	\n"""

	for suppFormat, features in canmatrix.formats.supportedFormats.items():
		usage += suppFormat + "\t"
		if 'load' in features:
			usage += "import"
		usage += "\n"

	parser = OptionParser(usage=usage)

	(cmdlineOptions, args) = parser.parse_args()
	if len(args) < 1:
		parser.print_help()
		sys.exit(1)

	infile = args[0]

	CANObj = toPyObject(infile, **cmdlineOptions.__dict__)

	createCosmosCmd(CANObj, "AMSAT_cmd.txt")
	createCosmosTlm(CANObj, "AMSAT_tlm.txt")
	createCosmosCmd(CANObj, "PEAK_CAN_cmd.txt")
	createCosmosTlm(CANObj, "PEAK_CAN_tlm.txt")


if __name__ == '__main__':
	sys.exit(main())
