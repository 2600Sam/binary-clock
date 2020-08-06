#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# copyleft 05-08-2020 Sam Sheeley
# decode 4 bit binary the below example = 5
# 8
# 4 *
# 2
# 1 *

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
import datetime
serial = spi(port=0, device=1, gpio=noop())
# rotate the display x3 so it can be read while in front of the crowpi
device = max7219(serial, cascaded=1,  block_orientation=0, rotate=3)
device.contrast(1 * 16)
# device is setup and ready.. yes, no, maybe, I dont know can you repeate the question

def face_display(bit_bucket): # display the IT's clock face of
    with canvas(device) as draw:
        for pix_col, binary in enumerate(bit_bucket):
            for pix_row, bit in enumerate(binary):
                draw.point((pix_col+1, pix_row+3), fill=int(bit))

def build_display(hour, minute, second): # fill the bit bucket with binary number
    bit_bucket = []
    string_hour = str(hour).zfill(2) # make everything 2 digits the convert both to 4 bit binary
    bit_bucket.extend(dec_to_bin(string_hour[count]) for count in range(0, 2))
    string_minute = str(minute).zfill(2)
    bit_bucket.extend(dec_to_bin(string_minute[count]) for count in range(0, 2))
    string_second = str(second).zfill(2)
    bit_bucket.extend(dec_to_bin(string_second[count]) for count in range(0, 2))
    face_display(bit_bucket) # actual dewing of it
    del bit_bucket[:] # empty the bucket 

def dec_to_bin(num):# return a 4 bit binary number
    return '{0:04b}'.format(int(num)).zfill(4)

def main():
    now = datetime.datetime.now()
    # prev_sec = datetime.datetime.now().second
    last_sec = now.second
    while(datetime.datetime.now().second == last_sec):
        pass
    while(True):
        now = datetime.datetime.now() # a different now required here, why? because! I don't know
        build_display(now.hour, now.minute, now.second) # dewit

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # clear the matrix for exit
        device.cleanup()
