###################################################################################################
# author:       Nathan Wacker (nathan.wacker@live.com)
#
# description:  This script parses data from the HuskySat-1 (HS-1) mission sourced from the AMSAT
#               data server.  The output format is (currently) a series of csv files, one per
#               packet type.  The full description of packets can be found here:
# https://github.com/UWCubeSat/DS1Ops/blob/master/COSMOS/flight/outputs/handbooks/telemetry_handbook.pdf
###################################################################################################


import sys
PYTHON_VER = sys.version_info.major

import csv
import time
import struct
import os.path
import tarfile

if PYTHON_VER == 3:
    import urllib.request
else:
    import urllib2

# data source (will not download if in the same directory)
t0_url    = 'https://www.amsat.org/tlm/ops/'
t0_file   = 'FOX6T0.txt'
data_url  = 'https://www.amsat.org/tlm/husky/'
data_file = 'serverlogs.tar.gz'
can_file  = 'FOX6canpacket.log'

###################################################################################################
###################################################################################################
###################################################################################################
# Data structures for parsing

# dictionary of resets to unix epoch
T0_dict = {}

# list of packets w/o definitions
pkt_ids_missing = set([])

# pkt_id -> { epoch -> [col_val1, ..., col_valn]}
parsed_data = {}

###################################################################################################
###################################################################################################
###################################################################################################
# Commonly duplicated conversions for packet definitions

# data conversion functions:
def bytes_to_uint(byte_str):
    number = 0
    data_length = len(byte_str)
    for i in range(data_length):
        number += int(byte_str[i]) * 256**(data_length - i - 1)
    return number

def bytes_to_int(byte_str):
    num = bytes_to_uint(byte_str)
    if (num & (1 << (8 * len(byte_str) - 1))) != 0:
        num -= (2**(8 * len(byte_str)))
    return num

def enum_conv(enum):
    return (lambda x: enum[bytes_to_uint(x)] if bytes_to_uint(x) in enum else bytes_to_uint(x))

# bit is the location (1 -> 8) of the bit to look for
def one_bit_enum_conv(enum, bit):
    if len(enum) != 2:
        raise Exception("enum passed to one_bit_enum_conv() must have length 2")
    return (lambda x: enum_conv(enum)([(bytes_to_uint(x) >> (bit - 1)) & 1]))

def bool_conv(bit):
    return one_bit_enum_conv({0: "False", 1: "True"}, bit)

def double_conv(x):
    if len(x) != 8:
        raise Exception("bit string passed to double_conv() must have length 8")
    x = [int(i) for i in x]
    if PYTHON_VER == 3:
        x = bytes(x)
    else:
        x = bytearray(x)
    return struct.unpack('>d', x)[0]

# simple data conversions
hex_str_conv         = lambda x: hex(bytes_to_uint(x))
msp_temp_conv        = lambda x: bytes_to_int(x) / 100.0
nt_conv              = lambda x: bytes_to_int(x) / 73.0
dipole_gain_conv     = lambda x: bytes_to_int(x) / 100.0
imu_conv             = lambda x: bytes_to_int(x) * 0.004375
sun_vec_conv         = lambda x: bytes_to_int(x) * 3.051757 / (10**5)
sun_angle_conv       = lambda x: bytes_to_int(x) * 60.0 / 32767
voltage_conv         = lambda x: bytes_to_uint(x) * 23.6 / 65535
node_voltage_conv    = lambda x: bytes_to_uint(x) * 0.004
current_conv         = lambda x: (bytes_to_uint(x) - 32767) / 3276.7
temp_sensor_conv     = lambda x: bytes_to_int(x) - 50
node_current_conv    = lambda x: bytes_to_int(x) / 327.68
acc_charge_conv      = lambda x: bytes_to_uint(x) * 17.0 / 24576.0
batt_voltage_conv    = lambda x: bytes_to_uint(x) * 7.21698125 / 4096
domain_current_conv  = lambda x: bytes_to_int(x) / 2048.0
met_conv             = lambda x: bytes_to_uint(x) >> 8
pnl_current_conv     = lambda x: bytes_to_int(x) * 1.5 / 32768
pnl_power_conv       = lambda x: bytes_to_int(x) * 3 / 3276.8
ppt_time_conv        = lambda x: bytes_to_uint(x) * 1.0 / (2**15)
camera_lsn_conv      = lambda x: hex((bytes_to_uint(x) & 0xf))
camera_msn_conv      = lambda x: hex((bytes_to_uint(x) >> 4) & 0xf)

# enums
reset_enum = {0x0: "No interrupt pending", 0x2: "Brownout (BOR)", 0x4: "RSTIFG RST/NMI (BOR)",
                0x6: "PMMSWBOR software BOR (BOR)", 0x8: "LPMx.5 wakeup (BOR)", 0xa: "Security violation (BOR)",
                0xc: "Reserved", 0xe: "SVSHIFG SVSH event (BOR)", 0x10: "Reserved",
                0x12: "Reserved", 0x14: "PMMSWPOR software POR (POR)", 0x16: "WDTIFG watchdog timeout (PUC)",
                0x18: "WDTPW password violation (PUC)", 0x1a: "FRCTLPW password violation (PUC)", 0x1c: "Uncorrectable FRAM bit error detection (PUC)",
                0x1e: "Peripheral area fetch (PUC)", 0x20: "PMMPW PMM password violation (PUC)", 0x22: "MPUPW MPU password violation (PUC)",
                0x24: "CSPW CS password violation (PUC)", 0x26: "MPUSEGIPIFG encapsulated IP memory segment violation (PUC)",
                0x28: "MPUSEGIIFG information memory segment violation (PUC)", 0x2a: "MPUSEG1IFG segment 1 memory violation (PUC)",
                0x2c: "MPUSEG2IFG segment 2 memory violation (PUC)", 0x2e: "MPUSEG3IFG segment 3 memory violation (PUC)"}

i2c_res_enum = {0: "No_Error", 1: "Start_Timeout", 2: "Stop_Timeout", 3: "NACK", 4: "Transmit_Timeout"}

# column definitions
h1_cols = [
    ("Temperature_Min", 10, 2, msp_temp_conv),
    ("Temperature_Max", 12, 2, msp_temp_conv),
    ("Temperature_Avg", 14, 2, msp_temp_conv),
    ("Last_Reset_Cause", 16, 1, enum_conv(reset_enum)),
    ("Reset_Count", 17, 1, bytes_to_uint)
]

h2_cols = [("CAN_Rx_Error", 10, 1, bytes_to_uint)]
dist_c_cols = lambda pd: [
    (pd+"_State", 10, 1, enum_conv({0: "On", 1: "Off_Manual", 2: "Off_Over-Current", 3: "Off_Batt_Undervoltage", 4: "Off_Initial"})),
    (pd+"_Current_Min", 11, 2, domain_current_conv),
    (pd+"_Current_Max", 13, 2, domain_current_conv),
    (pd+"_Current_Avg", 15, 2, domain_current_conv),
]

dist_v_cols = lambda pd: [
    (pd+"_Voltage_Min", 10, 2, node_voltage_conv),
    (pd+"_Voltage_Max", 12, 2, node_voltage_conv),
    (pd+"_Voltage_Avg", 14, 2, node_voltage_conv)
]
###################################################################################################
###################################################################################################
###################################################################################################

# this is the packet definition stucture
# id => (name, [columns1, column2, ... columnN])
# column == (name, start byte, length, conversion function)
# NOTE: some packets defs are missing because those packets were never received
#       and some numbered packets are missing for historical naming reasons
pkt_defs = {
    0x12570021: ("CMD_MTQ_BDOT", [
        ("X", 10, 1, bytes_to_int),
        ("Y", 11, 1, bytes_to_int),
        ("Z", 12, 1, bytes_to_int),
    ]),
    0x1204033a: ("COM1_MODE", [
        ("Mode", 10, 1, enum_conv({1: "Health", 2: "Safe", 3: "Real-Time", 4: "Camera"}))
    ]),
    0x12570030: ("MTQ_ACK", [
        ("Phase", 10, 1, enum_conv({0: "Measurement", 1: "Actuation", 2: "PMS"})),
        ("Source", 11, 1, enum_conv({0: "FSW", 1: "BDot"})),
        ("Last_BDot_X", 12, 1, bytes_to_int),
        ("Last_BDot_Y", 13, 1, bytes_to_int),
        ("Last_BDot_Z", 14, 1, bytes_to_int),
        ("Last_FSW_X", 15, 1, bytes_to_int),
        ("Last_FSW_Y", 16, 1, bytes_to_int),
        ("Last_FSW_Z", 17, 1, bytes_to_int)
    ]),
    0x12180320: ("RAHS_CAMERA", [
        # See https://bitbucket.org/Quick2space/mcp25625.py/src/master/docs/SSF-v03.pdf for more information
        ("X1", 10, 1, bytes_to_uint),
        ("Y1", 11, 1, bytes_to_uint),
        ("G1", 12, 1, camera_msn_conv),
        ("G2", 12, 1, camera_lsn_conv),
        ("G3", 13, 1, camera_msn_conv),
        ("G4", 13, 1, camera_lsn_conv),
        ("G5", 14, 1, camera_msn_conv),
        ("G6", 14, 1, camera_lsn_conv),
        ("G7", 15, 1, camera_msn_conv),
        ("G8", 15, 1, camera_lsn_conv),
        ("G9", 16, 1, camera_msn_conv),
        ("GA", 16, 1, camera_lsn_conv),
        ("Checksum", 17, 1, hex_str_conv)
    ]),

    0x12690264: ("BDOT_H1", h1_cols),
    0x1269026d: ("BDOT_H2", h2_cols),
    0x12590206: ("BDOT_1", [
        ("SPAM_On_X_MTQ_X", 10, 2, nt_conv),
        ("SPAM_On_X_MTQ_Y", 12, 2, nt_conv),
        ("SPAM_On_X_MTQ_Z", 14, 2, nt_conv),
        ("SPAM_On_Y_MTQ_X", 16, 2, nt_conv)
    ]),
    0x12590207: ("BDOT_2", [
        ("Mag_X_Min", 10, 2, nt_conv),
        ("Mag_X_Max", 12, 2, nt_conv),
        ("Mag_X_Avg", 14, 2, nt_conv),
        ("Mag_Y_Min", 16, 2, nt_conv)
    ]),
    0x12590219: ("BDOT_3", [
        ("Mag_Y_Max", 10, 2, nt_conv),
        ("Mag_Y_Avg", 12, 2, nt_conv),
        ("Mag_Z_Min", 14, 2, nt_conv),
        ("Mag_Z_Max", 16, 2, nt_conv)
    ]),
    0x1259021a: ("BDOT_4", [
        ("Mag_Z_Avg", 10, 2, nt_conv),
        ("SPAM_On_Y_MTQ_Y", 12, 2, nt_conv),
        ("SPAM_On_Y_MTQ_Z", 14, 2, nt_conv),
        ("Tumble_Status", 16, 1, one_bit_enum_conv({0: "Not Tumbling", 1: "Tumbling"}, 8))
    ]),
    0x1259025c: ("BDOT_5", [
        ("SPAM_On_Z_MTQ_X", 10, 2, nt_conv),
        ("SPAM_On_Z_MTQ_Y", 12, 2, nt_conv),
        ("SPAM_On_Z_MTQ_Z", 14, 2, nt_conv)
    ]),
    0x12590270: ("BDOT_6", [
        ("SPAM_Off_Time", 10, 2, bytes_to_uint),
        ("SPAM_On_Time", 12, 2, bytes_to_uint),
        ("SPAM_Control", 14, 1, one_bit_enum_conv({0: "SPAM_Disabled", 1: "SPAM_Enabled"}, 8)),
        ("Max_Tumble_Time", 14, 3, lambda x: (bytes_to_uint(x) >> 7) & 0xffff),
        ("Current_State", 16, 1, lambda x: enum_conv({0: "Normal_Mode", 1: "Sleep_Mode", 2: "Spam_Mag_Self_Test", 3: "SPAM"})([(bytes_to_uint(x) >> 5) & 3])),
        ("POP_Status_X", 16, 1, bool_conv(5)),
        ("POP_Status_Y", 16, 1, bool_conv(4)),
        ("POP_Status_Z", 16, 1, bool_conv(3)),
        ("Gain_Override_Status_X", 16, 1, bool_conv(2)),
        ("Gain_Override_Status_Y", 16, 1, bool_conv(1)),
        ("Gain_Override_Status_Z", 17, 1, bool_conv(8)),
        ("Mag_Control", 17, 1, lambda x: enum_conv({0: "BDot_Mode", 1: "SP1_Mode", 2: "SP2_Mode"})([(bytes_to_uint(x) >> 5) & 3]))
    ]),
    0x12690271: ("BDOT_7", [
        ("SPAM_Magnitude_X", 10, 1, bytes_to_int),
        ("SPAM_Magnitude_Y", 11, 1, bytes_to_int),
        ("SPAM_Magnitude_Z", 12, 1, bytes_to_int),
        ("SPAM_Off_X_MTQ_X", 13, 2, nt_conv),
        ("SPAM_Off_X_MTQ_Y", 15, 2, nt_conv),
        ("Dipole_Gain_X", 17, 1, dipole_gain_conv)
    ]),
    0x12690272: ("BDOT_8", [
        ("SPAM_Off_X_MTQ_Z", 10, 2, nt_conv),
        ("SPAM_Off_Y_MTQ_X", 12, 2, nt_conv),
        ("SPAM_Off_Y_MTQ_Y", 14, 2, nt_conv),
        ("SPAM_Off_Y_MTQ_Z", 16, 2, nt_conv)
    ]),
    0x12690273: ("BDOT_9", [
        ("SPAM_Off_Z_MTQ_X", 10, 2, nt_conv),
        ("SPAM_OFF_Z_MTQ_Y", 12, 2, nt_conv),
        ("SPAM_OFF_Z_MTQ_Z", 14, 2, nt_conv),
        ("Dipole_Gain_Y", 16, 1, dipole_gain_conv),
        ("Dipole_Gain_Z", 17, 1, dipole_gain_conv)
    ]),
    0x126902dd: ("BDOT_10", [
        ("Dipole_Variance_X", 10, 2, bytes_to_uint),
        ("Dipole_Variance_Y", 12, 2, bytes_to_uint),
        ("Dipole_Variance_Z", 14, 2, bytes_to_uint)
    ]),
    0x12690274: ("BDOT_11", [
        ("Magnetometer_X_Variance", 10, 2, bytes_to_uint),
        ("Magnetometer_Y_Variance", 12, 2, bytes_to_uint),
        ("Magnetometer_Z_Variance", 14, 2, bytes_to_uint)
    ]),

    0x12590261: ("ESTIM_H1", h1_cols),
    0x1259026a: ("ESTIM_H2", h2_cols),
    0x1259022d: ("ESTIM_2", [("Position_X", 10, 8, double_conv)]),
    0x1259022e: ("ESTIM_3", [("Position_Y", 10, 8, double_conv)]),
    0x1259022f: ("ESTIM_4", [("Position_Z", 10, 8, double_conv)]),
    0x12590230: ("ESTIM_5", [("Velocity_X", 10, 8, double_conv)]),
    0x12590231: ("ESTIM_6", [("Velocity_Y", 10, 8, double_conv)]),
    0x12590232: ("ESTIM_7", [("Velocity_Z", 10, 8, double_conv)]),
    0x12590233: ("ESTIM_8", [
        ("Epoch", 10, 5, met_conv),
        ("SGP4_Flag", 15, 1, bytes_to_int),
        ("Spacecraft_In_Sun", 16, 1, bool_conv(8)),
        ("Spacecraft_Above_Ground_Station", 16, 1, bool_conv(7)),
        ("TLE_ID_Valid", 16, 1, bool_conv(6))
    ]),
    0x12590254: ("ESTIM_9", [("Sun_X", 10, 8, double_conv)]),
    0x12590255: ("ESTIM_10", [("Sun_Y", 10, 8, double_conv)]),
    0x12590256: ("ESTIM_11", [("Sun_Z", 10, 8, double_conv)]),
    0x12590257: ("ESTIM_12", [("Mag_X", 10, 8, double_conv)]),
    0x12590258: ("ESTIM_13", [("Mag_Y", 10, 8, double_conv)]),
    0x12590259: ("ESTIM_14", [("Mag_Z", 10, 8, double_conv)]),

    0x12690262: ("MPC_H1", h1_cols),
    0x1269026b: ("MPC_H2", h2_cols),
    0x12590235: ("MPC_2", [("Spacecraft_Quaternion_1", 10, 8, double_conv)]),
    0x12590236: ("MPC_3", [("Spacecraft_Quaternion_2", 10, 8, double_conv)]),
    0x12590237: ("MPC_4", [("Spacecraft_Quaternion_3", 10, 8, double_conv)]),
    0x12590238: ("MPC_5", [("Spacecraft_Quaternion_4", 10, 8, double_conv)]),
    0x12590239: ("MPC_6", [("Omega_Min", 10, 8, double_conv)]),
    0x1259023a: ("MPC_7", [("Omega_Max", 10, 8, double_conv)]),
    0x1259023b: ("MPC_8", [("Omega_Avg", 10, 8, double_conv)]),
    0x1259023c: ("MPC_9", [("Omega_X", 10, 8, double_conv)]),
    0x1259023d: ("MPC_10", [("Omega_Y", 10, 8, double_conv)]),
    0x1259023e: ("MPC_11", [("Omega_Z", 10, 8, double_conv)]),
    0x12590242: ("MPC_15", [
        ("Spacecraft_Mode", 10, 1, bytes_to_int),
        ("Point_True", 11, 1, bytes_to_uint)
    ]),

    0x1269025e: ("MTQ_H1", h1_cols),
    0x12690267: ("MTQ_H2", h2_cols),
    0x1269020c: ("MTQ_2", [
        ("BDot_X_Avg", 10, 1, bytes_to_int),
        ("BDot_X_Max", 11, 1, bytes_to_int),
        ("BDot_X_Min", 12, 1, bytes_to_int),
        ("BDot_Y_Avg", 13, 1, bytes_to_int),
        ("BDot_Y_Max", 14, 1, bytes_to_int),
        ("BDot_Y_Min", 15, 1, bytes_to_int),
        ("BDot_Z_Avg", 16, 1, bytes_to_int),
        ("BDot_Z_Max", 17, 1, bytes_to_int),
    ]),
    0x1269020d: ("MTQ_3", [
        ("BDot_Z_Min", 10, 1, bytes_to_int),
        ("FSW_X_Avg", 11, 1, bytes_to_int),
        ("FSW_X_Max", 12, 1, bytes_to_int),
        ("FSW_X_Min", 13, 1, bytes_to_int),
        ("FSW_Y_Avg", 14, 1, bytes_to_int),
        ("FSW_Y_Max", 15, 1, bytes_to_int),
        ("FSW_Y_Min", 16, 1, bytes_to_int),
        ("FSW_Z_Avg", 17, 1, bytes_to_int),
    ]),
    0x1269020e: ("MTQ_4", [
        ("FSW_Z_Max", 10, 1, bytes_to_int),
        ("FSW_Z_Min", 11, 1, bytes_to_int),
        ("Duty_X1_Avg", 12, 1, bytes_to_uint),
        ("Duty_X2_Avg", 13, 1, bytes_to_uint),
        ("Duty_Y1_Avg", 14, 1, bytes_to_uint),
        ("Duty_Y2_Avg", 15, 1, bytes_to_uint),
        ("Duty_Z1_Avg", 16, 1, bytes_to_uint),
        ("Duty_Z2_Avg", 17, 1, bytes_to_uint),
    ]),
    0x1269020f: ("MTQ_5", [
        ("Ignore_FSW", 10, 1, enum_conv({0: "False", 1: "True"})),
        ("Reset_Counts", 11, 1, bytes_to_uint),
        ("Command_X_Variance", 12, 2, bytes_to_uint),
        ("Command_Y_Variance", 14, 2, bytes_to_uint),
        ("Command_Z_Variance", 16, 2, bytes_to_uint),
    ]),

    0x12690260: ("SP_H1", h1_cols),
    0x1259021c: ("SP_2", [
        ("IMU_Processed_X_Min", 10, 2, imu_conv),
        ("IMU_Processed_X_Max", 12, 2, imu_conv),
        ("IMU_Processed_X_Avg", 14, 2, imu_conv),
        ("IMU_Processed_Y_Min", 16, 2, imu_conv)
    ]),
    0x1259021d: ("SP_3", [
        ("IMU_Processed_Y_Max", 10, 2, imu_conv),
        ("IMU_Processed_Y_Avg", 12, 2, imu_conv),
        ("IMU_Processed_Z_Min", 14, 2, imu_conv),
        ("IMU_Processed_Z_Max", 16, 2, imu_conv)
    ]),
    0x1259021e: ("SP_4", [
        ("IMU_Processed_Z_Avg", 10, 2, imu_conv),
        ("Sun_X_Min", 12, 2, sun_vec_conv),
        ("Sun_X_Max", 14, 2, sun_vec_conv),
        ("Sun_X_Avg", 16, 2, sun_vec_conv),
    ]),
    0x1259021f: ("SP_5", [
        ("Sun_Y_Min", 10, 2, sun_vec_conv),
        ("Sun_Y_Max", 12, 2, sun_vec_conv),
        ("Sun_Y_Avg", 14, 2, sun_vec_conv),
        ("Sun_Z_Min", 16, 2, sun_vec_conv)
    ]),
    0x12590220: ("SP_6", [
        ("Sun_Z_Max", 10, 2, sun_vec_conv),
        ("Sun_Z_Avg", 12, 2, sun_vec_conv),
        ("Mag1_Valid", 14, 1, bytes_to_uint),
        ("Mag2_Valid", 15, 1, bytes_to_uint),
        ("Mag1_X_Min", 16, 2, nt_conv)
    ]),
    0x12590221: ("SP_7", [
        ("Mag1_Variance_X", 10, 2, bytes_to_uint),
        ("Mag1_Variance_Y", 12, 2, bytes_to_uint),
        ("Mag1_Variance_Z", 14, 2, bytes_to_uint),
    ]),
    0x12590222: ("SP_8", [
        ("Mag2_Variance_X", 10, 2, bytes_to_uint),
        ("Mag2_Variance_Y", 12, 2, bytes_to_uint),
        ("Mag2_Variance_Z", 14, 2, bytes_to_uint),
    ]),
    0x12590223: ("SP_9", [
        ("Mag1_X_Max", 10, 2, nt_conv),
        ("Mag1_X_Avg", 12, 2, nt_conv),
        ("Mag1_Y_Min", 14, 2, nt_conv),
        ("Mag1_Y_Max", 16, 2, nt_conv),
    ]),
    0x12590224: ("SP_10", [
        ("Mag1_Y_Avg", 10, 2, nt_conv),
        ("Mag1_Z_Min", 12, 2, nt_conv),
        ("Mag1_Z_Max", 14, 2, nt_conv),
        ("Mag1_Z_Avg", 16, 2, nt_conv),
    ]),
    0x12590225: ("SP_11", [
        ("Mag2_X_Min", 10, 2, nt_conv),
        ("Mag2_X_Max", 12, 2, nt_conv),
        ("Mag2_X_Avg", 14, 2, nt_conv),
        ("Mag2_Y_Min", 16, 2, nt_conv),
    ]),
    0x12590226: ("SP_12", [
        ("Mag2_Y_Max", 10, 2, nt_conv),
        ("Mag2_Y_Avg", 12, 2, nt_conv),
        ("Mag2_Z_Min", 14, 2, nt_conv),
        ("Mag2_Z_Max", 16, 2, nt_conv),
    ]),
    0x12590227: ("SP_13", [
        ("Mag2_Z_Avg", 10, 2, nt_conv),
        ("Sun_Alpha_Min", 12, 2, sun_angle_conv),
        ("Sun_Alpha_Max", 14, 2, sun_angle_conv),
        ("Sun_Alpha_Avg", 16, 2, sun_angle_conv)
    ]),
    0x12590228: ("SP_14", [
        ("Sun_Beta_Min", 10, 2, sun_angle_conv),
        ("Sun_Beta_Max", 12, 2, sun_angle_conv),
        ("Sun_Beta_Avg", 14, 2, sun_angle_conv),
        ("Sun_Valid", 16, 1, bytes_to_uint)
    ]),
    0x12590229: ("SP_15", [
        ("IMU_Valid", 10, 1, bytes_to_uint),
        ("IMU_X_Min", 11, 2, imu_conv),
        ("IMU_X_Max", 13, 2, imu_conv),
        ("IMU_X_Avg", 15, 2, imu_conv)
    ]),
    0x1259022a: ("SP_16", [
        ("IMU_Y_Min", 10, 2, imu_conv),
        ("IMU_Y_Max", 12, 2, imu_conv),
        ("IMU_Y_Avg", 14, 2, imu_conv),
        ("IMU_Z_Min", 16, 2, imu_conv)
    ]),
    0x1259022b: ("SP_17", [
        ("IMU_Z_Max", 10, 2, imu_conv),
        ("IMU_Z_Avg", 12, 2, imu_conv),
        ("I2C_Result_Mag1", 14, 1, enum_conv(i2c_res_enum)),
        ("I2C_Resumt_Mag2", 15, 1, enum_conv(i2c_res_enum)),
        ("I2C_Result_IMU", 16, 1, enum_conv(i2c_res_enum)),
        ("I2C_Result_Sun", 17, 1, enum_conv(i2c_res_enum))
    ]),

    0x12690265: ("BATT_H1", h1_cols),
    0x1269026e: ("BATT_H2", [
        ("CAN_Rx_Error", 10, 1, bytes_to_uint),
        ("Last_I2C_Result", 11, 1, enum_conv(i2c_res_enum))
    ]),
    0x12790200: ("BATT_1", [
        ("Accumulated_Charge_Avg", 10, 2, bytes_to_uint),
        ("Voltage_Avg", 12, 2, voltage_conv),
    ]),
    0x12690201: ("BATT_2", [
        ("Node_Voltage_Min", 10, 2, node_voltage_conv),
        ("Node_Voltage_Max", 12, 2, node_voltage_conv),
        ("Node_Voltage_Avg", 14, 2, node_voltage_conv)
    ]),
    0x12690202: ("BATT_3", [
        ("Current_Min", 10, 2, current_conv),
        ("Current_Max", 12, 2, current_conv),
        ("Current_Avg", 14, 2, current_conv),
        ("Battery_Temperature_Avg", 16, 1, temp_sensor_conv)
    ]),
    0x12590203: ("BATT_4", [
        ("Voltage_Min", 10, 2, voltage_conv),
        ("Voltage_Max", 12, 2, voltage_conv),
        ("Voltage_Avg", 14, 2, voltage_conv),
        ("Balancer_Enabled", 16, 1, bool_conv(8)),
        ("Heater_Enabled", 16, 1, bool_conv(7)),
        ("Heater_Automation_Enabled", 16, 1, bool_conv(6)),
        ("Balancer_Automation_Enabled", 16, 1, bool_conv(5))
    ]),
    0x12690204: ("BATT_5", [
        ("Node_Current_Min", 10, 2, node_current_conv),
        ("Node_Current_Max", 12, 2, node_current_conv),
        ("Node_Current_Avg", 14, 2, node_current_conv),
        ("Battery_Temperature_Min", 16, 1, temp_sensor_conv),
        ("Battery_Temperature_Max", 17, 1, temp_sensor_conv),
    ]),
    0x12690205: ("BATT_6", [
        ("Status", 10, 1, hex_str_conv),
        ("Control", 11, 1, hex_str_conv),
        ("Last_Charge_Time", 12, 5, lambda x: bytes_to_uint(x) / (2**8))
    ]),
    0x1259025a: ("BATT_7", [
        ("Accumulated_Charge_Min", 10, 2, acc_charge_conv),
        ("Accumulated_Charge_Max", 12, 2, acc_charge_conv),
        ("Accumulated_Charge_Avg", 14, 2, acc_charge_conv)
    ]),

    0x12690263: ("DIST_H1", h1_cols),
    0x1269026c: ("DIST_H2", h2_cols),
    0x12700243: ("DIST_1", [
        ("Battery_Voltage_Avg", 10, 2, batt_voltage_conv),
        ("COM1_Current_Avg", 12, 2, domain_current_conv),
        ("Temperature_Avg", 14, 2, msp_temp_conv)
    ]),
    0x12590244: ("DIST_2", [
        ("Under-Voltage_State", 10, 1, enum_conv({0: "Normal", 1: "Under_Voltage"})),
        ("MET", 11, 5, met_conv)
    ]),
    0x12590245: ("DIST_3", [
        ("Battery_Voltage_Min", 10, 2, batt_voltage_conv),
        ("Battery_Voltage_Max", 12, 2, batt_voltage_conv),
        ("Battery_Voltage_Avg", 14, 2, batt_voltage_conv),
    ]),
    0x12690246: ("DIST_4", dist_c_cols("COM1")),
    0x12590247: ("DIST_5", dist_v_cols("COM1")),
    0x12590248: ("DIST_6", dist_c_cols("COM2")),
    0x12590249: ("DIST_7", dist_v_cols("COM2")),
    0x1259024a: ("DIST_8", dist_c_cols("RAHS")),
    0x1259024b: ("DIST_9", dist_v_cols("RAHS")),
    0x1259024c: ("DIST_10", dist_c_cols("BDOT")),
    0x1259024d: ("DIST_11", dist_v_cols("BDOT")),
    0x1259024e: ("DIST_12", dist_c_cols("ESTIM")),
    0x1259024f: ("DIST_13", dist_v_cols("ESTIM")),
    0x12590250: ("DIST_14", dist_c_cols("EPS")),
    0x12590251: ("DIST_15", dist_v_cols("EPS")),
    0x12590252: ("DIST_16", dist_c_cols("PPT")),
    0x12590253: ("DIST_17", dist_v_cols("PPT")),
    0x125902db: ("DIST_18", [
        # each field here is 9 bits, so this ain't pretty
        ("BDOT_Over-Current_Threshold", 10, 2, lambda x: ((bytes_to_uint(x) >> 7) & 0x1ff) / 20.0),
        ("COM2_Over-Current_Threshold", 11, 2, lambda x: ((bytes_to_uint(x) >> 6) & 0x1ff) / 20.0),
        ("EPS_Over-Current_Threshold", 12, 2, lambda x: ((bytes_to_uint(x) >> 5) & 0x1ff) / 20.0),
        ("ESTIM_Over-Current_Threshold", 13, 2, lambda x: ((bytes_to_uint(x) >> 4) & 0x1ff) / 20.0),
        ("PPT_Over-Current_Threshold", 14, 2, lambda x: ((bytes_to_uint(x) >> 3) & 0x1ff) / 20.0),
        ("RAHS_Over-Current_Threshold", 15, 2, lambda x: ((bytes_to_uint(x) >> 2) & 0x1ff) / 20.0)
    ]),

    0x1269025f: ("GEN_H1", h1_cols),
    0x12690268: ("GEN_H2", h2_cols),
    0x12590210: ("GEN_1", [
        ("Panel_1_Enabled", 10, 1, bool_conv(8)),
        ("Panel_2_Enabled", 10, 1, bool_conv(7)),
        ("Panel_3_Enabled", 10, 1, bool_conv(6)),
        ("Panel_1_Charging", 10, 1, bool_conv(5)),
        ("Panel_2_Charging", 10, 1, bool_conv(4)),
        ("Panel_3_Charging", 10, 1, bool_conv(3)),
    ]),
    0x12590211: ("GEN_2", [
        ("Panel_1_Voltage_Min", 10, 2, node_voltage_conv),
        ("Panel_1_Voltage_Max", 12, 2, node_voltage_conv),
        ("Panel_1_Voltage_Avg", 14, 2, node_voltage_conv),
        ("Panel_2_Voltage_Min", 16, 2, node_voltage_conv)
    ]),
    0x12590212: ("GEN_3", [
        ("Panel_2_Voltage_Max", 10, 2, node_voltage_conv),
        ("Panel_2_Voltage_Avg", 12, 2, node_voltage_conv),
        ("Panel_3_Voltage_Min", 14, 2, node_voltage_conv),
        ("Panel_3_Voltage_Max", 16, 2, node_voltage_conv)
    ]),
    0x12590213: ("GEN_4", [
        ("Panel_3_Voltage_Avg", 10, 2, node_voltage_conv),
        ("Panel_1_Current_Min", 12, 2, pnl_current_conv),
        ("Panel_1_Current_Max", 14, 2, pnl_current_conv),
        ("Panel_1_Current_Avg", 16, 2, pnl_current_conv)
    ]),
    0x12590214: ("GEN_5", [
        ("Panel_2_Current_Min", 10, 2, pnl_current_conv),
        ("Panel_2_Current_Max", 12, 2, pnl_current_conv),
        ("Panel_2_Current_Avg", 14, 2, pnl_current_conv),
        ("Panel_3_Current_Min", 16, 2, pnl_current_conv),
    ]),
    0x12590215: ("GEN_6", [
        ("Panel_3_Current_Max", 10, 2, pnl_current_conv),
        ("Panel_3_Current_Avg", 12, 2, pnl_current_conv),
        ("Panel_1_Power_Min", 14, 2, pnl_power_conv),
        ("Panel_1_Power_Max", 16, 2, pnl_power_conv)
    ]),
    0x12590216: ("GEN_7", [
        ("Panel_1_Power_Avg", 10, 2, pnl_power_conv),
        ("Panel_2_Power_Min", 12, 2, pnl_power_conv),
        ("Panel_2_Power_Max", 14, 2, pnl_power_conv),
        ("Panel_2_Power_Avg", 16, 2, pnl_power_conv)
    ]),
    0x12590217: ("GEN_8", [
        ("Panel_3_Power_Min", 10, 2, pnl_power_conv),
        ("Panel_3_Power_Max", 12, 2, pnl_power_conv),
        ("Panel_3_Power_Avg", 14, 2, pnl_power_conv),
        ("Panel_1_Temperature_Min", 16, 1, temp_sensor_conv)
    ]),
    0x12590218: ("GEN_9", [
        ("Panel_1_Temperature_Max", 10, 1, temp_sensor_conv),
        ("Panel_1_Temperature_Avg", 11, 1, temp_sensor_conv),
        ("Panel_2_Temperature_Min", 12, 1, temp_sensor_conv),
        ("Panel_2_Temperature_Max", 13, 1, temp_sensor_conv),
        ("Panel_2_Temperature_Avg", 14, 1, temp_sensor_conv),
        ("Panel_3_Temperature_Min", 15, 1, temp_sensor_conv),
        ("Panel_3_Temperature_Max", 16, 1, temp_sensor_conv),
        ("Panel_3_Temperature_Avg", 17, 1, temp_sensor_conv)
    ]),
    0x12790332: ("GEN_10", [
        ("Panel_1_Power_Avg", 10, 2, pnl_power_conv),
        ("Panel_2_Power_Avg", 12, 2, pnl_power_conv),
        ("Panel_3_Power_Avg", 14, 2, pnl_power_conv)
    ]),

    0x1269025d: ("PPT_H1", h1_cols),
    0x12690266: ("PPT_H2", [
        ("CAN_Rx_Error", 10, 1, bytes_to_uint),
        ("Last_Fire_Result", 11, 1, lambda x: enum_conv({0: "Fire_Successful", 1: "No_Main_Charge", 2: "No_Main_Discharge"})([(bytes_to_uint(x) >> 6) & 3]))
    ]),
    0x12590208: ("PPT_1", [
        ("Fire_Count", 10, 2, bytes_to_uint),
        ("Fault_Count", 12, 2, bytes_to_uint),
        ("Last_Main_Charge_Time", 14, 2, ppt_time_conv),
        ("SMT_Wait_Time", 16, 2, ppt_time_conv)
    ]),
    0x12590209: ("PPT_2", [
        ("Main_Charge_Time", 10, 2, ppt_time_conv),
        ("Main_Ignited_Delay_Time", 12, 2, ppt_time_conv),
        ("Igniter_Charge_Time", 14, 2, ppt_time_conv),
        ("Cooldown_Time", 16, 2, ppt_time_conv)
    ]),
}

###################################################################################################
###################################################################################################
###################################################################################################
# Main program functions

# returns the unix epoch time for a given satellite reset and uptime
def get_epoch_for_sat_time(reset, uptime):
    if reset not in T0_dict:
        raise Exception('error: reset (' + str(reset) + ') more recent than last recorded time - delete FOX6T0.txt and re-run')
    return int(T0_dict[reset]/1000) + uptime

# download a single file from src and write to disk at dst
def download(src, dst):
    if PYTHON_VER == 3:
        urllib.request.urlretrieve(src, dst)
    else:
        raw_data = urllib2.urlopen(src).read()

        with open(dst, 'wb') as dst_file:
            dst_file.write(raw_data)

# download the source data from AMSAT
def download_data():
    # check for T0 file
    if os.path.isfile("./" + t0_file):
        print("using existent " + t0_file)
    else:
        print("downloading " + t0_file + "...")
        download(t0_url + t0_file, t0_file)

    # check for CAN data file
    if os.path.isfile('./' + can_file):
        print("using existent " + can_file)
    else:
        if not os.path.isfile('./' + data_file):
            print("downloading " + data_file + "...")
            download(data_url + data_file, data_file)
        else:
            print("using existent " + data_file)
        
        print("extracting " + can_file + "...")
        archive = tarfile.open(data_file, "r:gz")
        archive.extractall()
        archive.close()

# parse the data to memory based on packet definitions
def parse_data():
    # load the T0 dictionary
    # these are the reset times for COM1 (needed for unix epoch conversion)
    with open(t0_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            T0_dict[int(row[0])] = int(row[1])
    
    # read the data csv
    with open(can_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            canId = row[6:10]
            numericId = 0
            for i in range(len(canId)):
                numericId += int(canId[i]) * 256**i
            numericId &= 2**29-1
            reset = int(row[2])
            uptime = int(row[3])
            if reset == 65535:
                # this is some special data that we want to ignore
                continue

            epoch = get_epoch_for_sat_time(reset, uptime)
            
            if numericId in pkt_defs:
                # add packet to parsed_data
                if numericId not in parsed_data:
                    parsed_data[numericId] = {}
                
                # add timestamp to pkt_defs
                parsed_data[numericId][epoch] = []

                columns = pkt_defs[numericId][1]
                for i in range(len(columns)):
                    _,start_byte,length,conv = columns[i]
                    converted_value = conv(row[start_byte:start_byte+length])
                    parsed_data[numericId][epoch].append(str(converted_value))
            else:
                pkt_ids_missing.add(numericId)

    for idnum in pkt_ids_missing:
        print("!!! no definition for packet with id [" + hex(idnum) + "] found")

# write parsed data to csv files
def output_csv():
    for pkt_id in pkt_defs:
        pkt_name = pkt_defs[pkt_id][0]
        with open(pkt_name+".csv", "w") as csvfile:
            # write column names
            csvfile.write("time")
            for i in range(len(pkt_defs[pkt_id][1])):
                col_name,_,_,_ = pkt_defs[pkt_id][1][i]
                csvfile.write(","+col_name)
            csvfile.write("\n")

            # write the records
            for epoch in sorted(parsed_data[pkt_id]):
                csvfile.write(str(epoch))
                for col_val in parsed_data[pkt_id][epoch]:
                    csvfile.write("," + str(col_val))
                csvfile.write("\n")

# main
if __name__ == "__main__":
    download_data()

    print("parsing data...")
    parse_data()

    print("writing output...")
    output_csv()
