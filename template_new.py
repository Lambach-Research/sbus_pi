import read_sbus_from_GPIO
import time
from sbus_writer import SbusWriter  # Assuming the SbusWriter class is in a file named sbus_writer.py

SBUS_PIN = 4  # pin where sbus wire is plugged in

reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
reader.begin_listen()

writer = SbusWriter(SBUS_PIN)  # Create an instance of the SbusWriter class

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
        # ex:print(f'{channel_data[0]}')
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