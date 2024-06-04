import pigpio
import bitarray as ba
import bitarray.util as bau
import time

class SbusWriter:
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin #BCM pin
        self.pi = pigpio.pi()
        self.pi.set_mode(gpio_pin, pigpio.OUTPUT)

    def send_packet(self, channel_values):
        # Create an empty SBUS packet
        packet = ba.bitarray(25*8) # SBUS packets are 25 bytes long

        # Set the start byte of the SBUS packet
        packet[0:8] = ba.bitarray('11110000')

        # For each channel value, convert the value to binary, invert the bits, and add the bits to the SBUS packet
        for i, value in enumerate(channel_values):
            # Convert the value to binary and invert the bits
            binary_value = ba.bitarray(bin(value)[2:].zfill(11), endian='little')
            inverted_value = ~binary_value

            # Add the inverted bits to the SBUS packet
            packet[8+i*11:8+(i+1)*11] = inverted_value

        # Calculate the parity bit for the SBUS packet and add it to the packet
        parity_bit = bau.parity(packet[8:8+16*11])
        packet[8+16*11] = parity_bit

        # Set the end byte of the SBUS packet
        packet[-8:] = ba.bitarray('00000000')

        # Send the SBUS packet over the GPIO pin
        self.pi.wave_add_serial(self.gpio_pin, 100000, packet.tobytes())
        wave_id = self.pi.wave_create()
        self.pi.wave_send_once(wave_id)
        while self.pi.wave_tx_busy():
            time.sleep(0.01)
        self.pi.wave_delete(wave_id)