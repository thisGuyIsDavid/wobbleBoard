#!/usr/bin/python
import smbus
import math
import time

# Register
power_mgmt_1 = 0x6b


def read_byte(reg):
    return bus.read_byte_data(address, reg)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg + 1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def get_z_rotation(x, y, z):
    radians = math.atan2(z, dist(y, x))
    return math.degrees(radians)


bus = smbus.SMBus(1)
address = 0x68

bus.write_byte_data(address, power_mgmt_1, 0)
while True:
    x_scaled = read_word_2c(0x3b) / 16384.0
    y_scaled = read_word_2c(0x3d) / 16384.0
    z_scaled = read_word_2c(0x3f) / 16384.0

    x_rotation = get_x_rotation(x_scaled, y_scaled, z_scaled)
    y_rotation = get_y_rotation(x_scaled, y_scaled, z_scaled)
    z_rotation = get_z_rotation(x_scaled, y_scaled, z_scaled)

    print(x_rotation, y_rotation, z_rotation)

    time.sleep(.5)