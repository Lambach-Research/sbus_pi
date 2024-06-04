import read_sbus_from_GPIO
import time
from sbus_writer import SbusWriter  # Assuming the SbusWriter class is in a file named sbus_writer.py

WRITE_PIN = 4  # pin where sbus wire is plugged in to send data
READ_PIN = 27  # pin where sbus wire is plugged in to read data

reader = read_sbus_from_GPIO.SbusReader(READ_PIN) 
reader.begin_listen()

writer = SbusWriter(WRITE_PIN)

# wait until connection is established
while(not reader.is_connected()):
    time.sleep(.2)

# Note that there will be nonsense data for the first 10ms or so of connection
# until the first packet comes in.
time.sleep(.1)

while True:
    try:
        is_connected = reader.is_connected()
        packet_age = reader.get_latest_packet_age()  # milliseconds

        # returns list of length 16, so -1 from channel num to get index
        channel_data = reader.translate_latest_packet()

        #
        # Do something with data here!
        print(f'I received {channel_data[0]}')
        #

        # Send the channel data over SBUS
        writer.send_packet(channel_data)

    except KeyboardInterrupt:
        # cleanup cleanly after ctrl-c
        reader.end_listen()
        writer.end_listen()  # Clean up the writer as well
        exit()
    except:
        # cleanup cleanly after error
        reader.end_listen()
        writer.end_listen()  # Clean up the writer as well
        raise