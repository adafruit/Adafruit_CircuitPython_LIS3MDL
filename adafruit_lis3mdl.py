# The MIT License (MIT)
#
# Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_lis3mdl`
================================================================================

CircuitPython helper library for the LIS3MDL 3-axis magnetometer

* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**
* Adafruit `Adafruit LSM6DS33 + LIS3MDL - 9 DoF IMU
<https://www.adafruit.com/product/4485>`_ (Product ID: 4485)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases


* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LSM6DSOX.git"


_LIS3MDL_DEFAULT_ADDRESS = const(0x1C)

_LIS3MDL_CHIP_ID = const(0x3D)

_LIS3MDL_WHOAMI = const(0xF)


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL.git"

_LIS3MDL_WHO_AM_I = const(0x0F)  # Register that contains the part ID
_LIS3MDL_CTRL_REG1 = const(0x20) # Register address for control 1
_LIS3MDL_CTRL_REG2 = const(0x21) # Register address for control 2
_LIS3MDL_CTRL_REG3 = const(0x22) # Register address for control 3
_LIS3MDL_CTRL_REG4 = const(0x23) # Register address for control 3
_LIS3MDL_OUT_X_L = const(0x28)   # Register address for X axis lower byte
_LIS3MDL_INT_CFG = const(0x30)   # Interrupt configuration register
_LIS3MDL_INT_THS_L = const(0x32) # Low byte of the irq threshold

_GAUSS_TO_MT = 0.1 #1 Gauss [G] =   0.1 Millitesla [mT]

# /** The magnetometer ranges */
# typedef enum {
#   LIS3MDL_RANGE_4_GAUSS = 0b00,  ///< +/- 4g (default value)
#   LIS3MDL_RANGE_8_GAUSS = 0b01,  ///< +/- 8g
#   LIS3MDL_RANGE_12_GAUSS = 0b10, ///< +/- 12g
#   LIS3MDL_RANGE_16_GAUSS = 0b11, ///< +/- 16g
# } lis3mdl_range_t;


# lis3mdl_range_t range = getRange();
# float scale = 1; // LSB per gauss
# if (range == LIS3MDL_RANGE_16_GAUSS)
#     scale = 1711;
# if (range == LIS3MDL_RANGE_12_GAUSS)
#     scale = 2281;
# if (range == LIS3MDL_RANGE_8_GAUSS)
#     scale = 3421;
# if (range == LIS3MDL_RANGE_4_GAUSS)
#     scale = 6842;


# /** The magnetometer data rate, includes FAST_ODR bit */
# typedef enum {
#   LIS3MDL_DATARATE_0_625_HZ = 0b0000, ///<  0.625 Hz
#   LIS3MDL_DATARATE_1_25_HZ = 0b0010,  ///<  1.25 Hz
#   LIS3MDL_DATARATE_2_5_HZ = 0b0100,   ///<  2.5 Hz
#   LIS3MDL_DATARATE_5_HZ = 0b0110,     ///<  5 Hz
#   LIS3MDL_DATARATE_10_HZ = 0b1000,    ///<  10 Hz
#   LIS3MDL_DATARATE_20_HZ = 0b1010,    ///<  20 Hz
#   LIS3MDL_DATARATE_40_HZ = 0b1100,    ///<  40 Hz
#   LIS3MDL_DATARATE_80_HZ = 0b1110,    ///<  80 Hz
#   LIS3MDL_DATARATE_155_HZ = 0b0001,   ///<  155 Hz (FAST_ODR + UHP)
#   LIS3MDL_DATARATE_300_HZ = 0b0011,   ///<  300 Hz (FAST_ODR + HP)
#   LIS3MDL_DATARATE_560_HZ = 0b0101,   ///<  560 Hz (FAST_ODR + MP)
#   LIS3MDL_DATARATE_1000_HZ = 0b0111,  ///<  1000 Hz (FAST_ODR + LP)
# } lis3mdl_dataRate_t;

# /** The magnetometer performance mode */
# typedef enum {
#   LIS3MDL_LOWPOWERMODE = 0b00,  ///< Low power mode
#   LIS3MDL_MEDIUMMODE = 0b01,    ///< Medium performance mode
#   LIS3MDL_HIGHMODE = 0b10,      ///< High performance mode
#   LIS3MDL_ULTRAHIGHMODE = 0b11, ///< Ultra-high performance mode
# } lis3mdl_performancemode_t;

# /** The magnetometer operation mode */
# typedef enum {
#   LIS3MDL_CONTINUOUSMODE = 0b00, ///< Continuous conversion
#   LIS3MDL_SINGLEMODE = 0b01,     ///< Single-shot conversion
#   LIS3MDL_POWERDOWNMODE = 0b11,  ///< Powered-down mode
# } lis3mdl_operationmode_t;

class LIS3MDL:
    """Driver for the LIS3MDL 3-axis magnetometer.
        :param ~busio.I2C i2c_bus: The I2C bus the LIS3MDL is connected to.
        :param address: The I2C slave address of the sensor
    """
    _chip_id = ROUnaryStruct(_LIS3MDL_WHOAMI, "<b")

    _perf_mode = RWBits(2, _LIS3MDL_CTRL_REG1, 5)
    _z_perf_mode = RWBits(2, _LIS3MDL_CTRL_REG4, 2)

    _operation_mode = RWBits(2, _LIS3MDL_CTRL_REG3, 0)

    _data_rate = RWBits(3, _LIS3MDL_CTRL_REG1, 2)

    _raw_mag_data = Struct(_LIS3MDL_OUT_X_L, "<hhh")

    _range = RWBits(2, _LIS3MDL_CTRL_REG2, 5)

    def __init__(self, i2c_bus, address=_LIS3MDL_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        if self._chip_id != _LIS3MDL_CHIP_ID:
            raise RuntimeError("Failed to find LIS3MDL - check your wiring!")
        self.reset()
        #   // set high quality performance mode
        # setPerformanceMode(LIS3MDL_ULTRAHIGHMODE);
        self._perf_mode = 0b11
        self._z_perf_mode = 0b11
        # // 155Hz default rate
        # setDataRate(LIS3MDL_DATARATE_155_HZ);

        # // lowest range
        # setRange(LIS3MDL_RANGE_4_GAUSS);
        self._range = 0

        # setOperationMode(LIS3MDL_CONTINUOUSMODE);
        self._operation_mode = 0
    def reset(self): #pylint: disable=no-self-use
        """Reset the sensor to the default state set by the library"""

        print("reeeset")

    @property
    def magnetic(self):
        """How do they even work?!"""

        raw_mag_data = self._raw_mag_data
        x = self._scale_mag_data(raw_mag_data[0]) * _GAUSS_TO_MT
        y = self._scale_mag_data(raw_mag_data[1]) * _GAUSS_TO_MT
        z = self._scale_mag_data(raw_mag_data[2]) * _GAUSS_TO_MT
        return(x, y, z)
    def _scale_mag_data(self, raw_measurement): #pylint: disable=no-self-use

        scale = 6842
        return raw_measurement/scale
