""" Test Each Data Rate """
import time
import board
import busio
from adafruit_lis3mdl import LIS3MDL, Rate

i2c = busio.I2C(board.SCL, board.SDA)
sensor = LIS3MDL(i2c)

current_rate = Rate.RATE_2_5_HZ #pylint: disable=no-member

sensor.data_rate = current_rate

while True:
    mag_x, mag_y, mag_z = sensor.magnetic

    print('X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT'.format(mag_x, mag_y, mag_z))

    # sleep for enough time so that we'll read the value twice per measurement
    sleep_time = (1/(Rate.string[current_rate]*2))
    time.sleep(sleep_time)
