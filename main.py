#!/usr/bin/python
import smbus
import math
import time
import sqlite3
import datetime

#   CREATE TABLE wobble_readings(id INTEGER PRIMARY KEY AUTOINCREMENT, x NUMERIC, y NUMERIC, z NUMERIC, insert_time TEXT);


class WobbleReader:

    def __init__(self):
        self.last_key = None
        self.bus = smbus.SMBus(1)
        self.address = 0x68
        self.bus.write_byte_data(0x68, 0x6b, 0)
        self.conn = sqlite3.connect('sensordata.db')

    def read_byte(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def read_word(self, reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg + 1)
        value = (h << 8) + l
        return value

    def read_word_2c(self, reg):
        val = self.read_word(reg)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    @staticmethod
    def dist(a, b):
        return math.sqrt((a * a) + (b * b))

    @staticmethod
    def get_y_rotation(x, y, z):
        radians = math.atan2(x, WobbleReader.dist(y, z))
        return -math.degrees(radians)

    @staticmethod
    def get_x_rotation(x, y, z):
        radians = math.atan2(y, WobbleReader.dist(x, z))
        return math.degrees(radians)

    @staticmethod
    def get_z_rotation(x, y, z):
        radians = math.atan2(z, WobbleReader.dist(y, x))
        return math.degrees(radians)

    def insert(self, x, y, z):
        c = self.conn.cursor()
        c.execute(
            """
            INSERT INTO wobble_readings(
            x, y, z, insert_time
            ) VALUES (
            %s, %s, %s, '%s'
            )""" % (x, y, z, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        self.conn.commit()

    def process(self):
        while True:
            x_scaled = self.read_word_2c(0x3b) / 16384.0
            y_scaled = self.read_word_2c(0x3d) / 16384.0
            z_scaled = self.read_word_2c(0x3f) / 16384.0

            x_rotation = self.get_x_rotation(x_scaled, y_scaled, z_scaled)
            y_rotation = self.get_y_rotation(x_scaled, y_scaled, z_scaled)
            z_rotation = self.get_z_rotation(x_scaled, y_scaled, z_scaled)

            #   set keys
            key = "%s_%s_%s" % (x_rotation, y_rotation, z_rotation)
            if self.last_key == key:
                continue
            else:
                self.last_key = key

            self.insert(x_rotation, y_rotation, z_rotation)
            time.sleep(.25)

    def run(self):
        try:
            self.process()
        except KeyboardInterrupt:
            pass
        finally:
            self.bus.close()
            self.conn.close()

WobbleReader().run()