__author__ = 'beau'

import pyb
from MAX31885 import MAX31885

tc=MAX31885(CS_pin='X5',SO_pin='X3',SCK_pin='X4')


def main():
    while True:#sw_state:
        print(tc.read())
        pyb.delay(50)

main()
