from __future__ import division
import math
from ax25 import *
from sat_config import *

def bin_to_hex(bin_inp):
    '''
    Return the HEX of the Binary Input.
    '''
    hex_res = hex(int(bin_inp, 2)).split("x")[1].upper()
    return hex_res


def dec_to_bin_readable(dec,length):
    '''
    Return the readable BIN format of the given decimal
    number with given bit length
    '''
    temp = '{0:0{1}b}'.format(dec,length)
    return temp

def hex_to_padded_binary(hex_inp):
    '''
    Return Padded Binary String of input HEX string
    '''
    hexadecimal = hex_inp
    end_length = len(hexadecimal) * 4
    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    return padded_binary

def create_epic_frame(payload,payload_str):
    '''
    Returns EPIC FRAME IN HEX
    '''
    command_token_bin = dec_to_bin_readable(COMMAND_TOKEN,8)
    src_id_bin = dec_to_bin_readable(src_satid,6)
    dest_id_bin = dec_to_bin_readable(dest_satid,6)
    src_mcu_bin = dec_to_bin_readable(src_mcu,6)
    dest_mcu_bin = dec_to_bin_readable(dest_mcu,6)
    command_source_bin = dec_to_bin_readable(1,1)
    command_type_bin = dec_to_bin_readable(command_type,7)
    command_length_bin = dec_to_bin_readable(command_length,8)

    epic_crc = ax25_crc_16_x25(payload)
    epic_crc_bin = "{:08b}".format(int(epic_crc.hex(),16))

    ## PAYLOAD BIN
    payload_bin = hex_to_padded_binary("".join(payload_str.split()).lower())

    ## COMMAND HEADER
    command_header_bin =src_id_bin + dest_id_bin + src_mcu_bin + dest_mcu_bin + command_source_bin + command_type_bin + command_length_bin 

    ## FINAL EPIC FRAME
    final_epic_frame_hex = bin_to_hex(command_token_bin) + bin_to_hex(command_header_bin) + bin_to_hex(payload_bin) + bin_to_hex(epic_crc_bin) + bin_to_hex(command_token_bin)


    print()
    print("************* EPIC FRAME DISECTED [BINARY] *************************")
    print("{:20s} : {}".format("COMMAND TOKEN ",command_token_bin))
    print("{:20s} : {}".format("SRC ID ",src_id_bin))
    print("{:20s} : {}".format("DEST ID ",dest_id_bin))
    print("{:20s} : {}".format("SRC MCU ",src_mcu_bin))
    print("{:20s} : {}".format("DEST MCU ",dest_mcu_bin))
    print("{:20s} : {}".format("COMMAND SOURCE ",command_source_bin))
    print("{:20s} : {}".format("COMMAND TYPE ",command_type_bin))
    print("{:20s} : {}".format("COMMAND LENGTH ",command_length_bin))
    print()


    return final_epic_frame_hex




