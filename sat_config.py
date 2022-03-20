'''
CONFIG
'''
dest_ssid                       = 1         # Destination Satellite ssid
dest_satid                      = 1         # Destination Satellite ID
dest_mcu                        = 1         # Destination satellite MCU
dest_callsign                    = "ES5E"    # Destination Call Sign
session_id                      = 1         # session ID

src_ssid                        = 10        # Source Satellite ssid 
src_satid                       = 10        # Source Satellite ID
src_mcu                         = 5         # Source satellite MCU
src_callsign                    = "PICO"    # Source Call Sign

command_length                  = 52        # Command Length
command_type                    = 7         # Command Type

COMMAND_TOKEN                   = 85        # SET GLOBAL COMMAND TOKEN = 0x55  

include_ssid                    = "n"       # DO WE INCLUDE SSID [y=True, n=False, Default=False]
