Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-lis3mdl/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/lis3mdl/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/actions
    :alt: Build Status

CircuitPython helper library for the LIS3MDL 3-axis magnetometer


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-lis3mdl/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-lis3mdl

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-lis3mdl

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-lis3mdl

Usage Example
=============

.. code-block:: python

    import time
    import board
    import busio
    import adafruit_lis3mdl

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_lis3mdl.LIS3MDL(i2c)

    while True:
        mag_x, mag_y, mag_z = sensor.magnetic

        print('X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT'.format(mag_x, mag_y, mag_z))
        print('')
        time.sleep(1.0)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_LIS3MDL/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
