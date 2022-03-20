from __future__ import division
import math
from datetime import datetime
from ax25 import *
from epic import *
from sat_config import *
import random
import time

def generate_sine_table(length=1024): 
    '''
    Creates The Sine Wave Payload
    '''   
    raw_table = []  
    for index, item in enumerate((random.random()/100+math.sin(2*math.pi*i/length) for i in range(length))):

        if math.modf(item)[0] > 0.5:
            value = hex(int(math.ceil((item*0xFF))))
        else:
            value = hex(int(math.floor((item*0xFF))))
        if divmod(index+1, 16)[-1]:
           raw_table.append(hex(int(item*0xFF)))
        else:
           raw_table.append(hex(int(item*0xFF)) + '\n')
           
    output_table = []    
    for item in (raw_table[j:j+16] for j in range(0, len(raw_table), 16)):
        output_table.append(' '.join(item))
    
    semi_output = ''.join(output_table)
    
    final_payload=[]
    for i in range(command_length):
        x = semi_output.split()[i]
        fg = x.split("x")[1].upper()
        if len(fg) >1:
            final_payload.append(fg)
            
    print(len(final_payload))
    if len(final_payload) < command_length:
        for d in range(command_length-len(final_payload)):
            final_payload.append(str(random.randint(10,28)))
    print(len(final_payload))
    payload_str=" ".join(final_payload)
    return final_payload,payload_str
    

def main():

    f = open("frames.txt", "w")
    f1 = open("pipes.txt", "w")
    
    for i in range(10):
        '''
        datetime object containing current date and time
        '''
        now = datetime.now()
        now = now.strftime('%Y-%m-%dT%H:%M:%SZ')


        '''
        CUSTOM PAYLOAD GENERATION
        '''
        final_payload,payload_str = generate_sine_table()

        payload = bytearray.fromhex(payload_str)
        print()
        print("*****************   PAYLOAD DATA            ***************************")
        print(final_payload)
        print()

        '''
        CREATE EPIC FRAME FROM PAYLOAD
        '''
        epic_frame = create_epic_frame(payload,payload_str)


        '''
        Create Data fRame AX.25
        '''
        ## AX25 CONFIG
        ax25_conf = {"use_modulo8": True, "set_pf_bit": False, "pid_field": AX25_PID_Fields.AX25_PID_NO_LAYER3}
        created_packet = ax25_create_frame(include_ssid,dest_callsign, dest_ssid, src_callsign, src_ssid, AX25_Ctrl_Fields.AX25_CTRL_UI,
            payload, **ax25_conf) 


        ## AX25 FRAME CLEANING [CUSTOM]
        data_frame = []
        for byte in created_packet:
            data_frame.append('{:02x}'.format(byte).upper())

        ## FLAG
        flag_hex = data_frame[0]
        ## DESTINATION CALL SIGN
        dest_callsign_hex = "".join(data_frame[1:8])

        ## SOURCE CALL SIGN
        src_callsign_hex = "".join(data_frame[8:15])

        ## FRAME CHECK CRC
        frame_check_hex = "".join(data_frame[-3:-1])

        ## CONTROL BITS
        ctrl_hex = "".join(data_frame[15])

        ## PROTOCOL IDENTIFIER
        pid_hex = "".join(data_frame[16])

        ## AX25 TRANSFER HEADER FRAME
        ax25_header_hex = "".join(data_frame[:17])

        ## AX25 TRANSFER TAIL FRAME
        ax25_tail_hex = "".join(data_frame[-3:])


        

        ## FINAL AX25 with EPIC
        ax25_epic_full = ax25_header_hex + epic_frame + ax25_tail_hex
        original_ax25 = ax25_epic_full
        ax25_epic_full = ax25_epic_full + " --tmstamp " + now + " " + src_callsign



        
        
        print()
        print("*****************   AX25 HEADER FRAME DISSECTED ***********************")
        print("{:20s} : {}".format("FLAG",flag_hex))
        print("{:20s} : {}".format("DEST CALLSIGN ",dest_callsign_hex))
        print("{:20s} : {}".format("SRC CALLSIGN ",src_callsign_hex))
        print("{:20s} : {}".format("CONTROL BITS ",ctrl_hex))
        print("{:20s} : {}".format("PROTOCOL IDENTIFIER ",pid_hex))
        print()

        print()
        print("******************* AX25 TAIL FRAME DISSECTED *************************")
        print("{:20s} : {}".format("FRAME CHECK CRC ",frame_check_hex))
        print("{:20s} : {}".format("FLAG",flag_hex))
        print()


        print("///////////////////////////////////////////////////////////////////////")
        print("                       FINAL FRAMES                                    ")
        print("///////////////////////////////////////////////////////////////////////")
        print()
        print("***************   EPIC DATA FRAME         *****************************")
        print(epic_frame)
        print()
        print("***************   AX.25 + EPIC DATA FRAME *****************************")
        print(ax25_epic_full)
        
        f.writelines("******************\n")
        f.writelines("Time :" +now +"\n")
        f.writelines("******************\n\n")
        
        f.writelines("Payload\n")
        f.writelines("_______________________________________________\n")
        f.writelines(" ".join(final_payload)+"\n\n")
        
        f.writelines("Old Format\n")
        f.writelines("_______________________________________________\n")
        f.writelines(ax25_epic_full+"\n\n")
        
        now = now[:10] +" " + now[11:-1]
        f.writelines("Pipe Format\n")
        f.writelines("_______________________________________________\n")
        f.writelines(now+"|"+original_ax25+"\n")
        f1.writelines(now+"|"+original_ax25+"\n")
        
        f.writelines("\n\n\n")
        
        
        
        print()
        print("***************   AX.25 DISSAMBLED DATA FRAME *************************")
        disassembled_frame = ax25_disassemble_raw_frame(created_packet)
        print(disassembled_frame)
        
        time.sleep(10)
        
    f.close()
    f1.close()

if __name__ == '__main__':
    main()