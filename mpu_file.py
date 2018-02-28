#!/usr/bin/python

import smbus
import math
import time

# Firebase added
import pyrebase

config = {
    "apiKey": "AIzaSyBYpa-62ef-3h7QxclH_jJCxjWi0uxyOlc",
    "authDomain": "road-analysis-pi.firebaseapp.com",
    "databaseURL": "https://road-analysis-pi.firebaseio.com",
    "storageBucket": "road-analysis-pi.appspot.com"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

road_uid = str(int(round(time.time() * 1000)))

while(1):
    bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
    address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    time.sleep(1)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    #print (gyro_xout, (gyro_xout / 131) , gyro_yout,  (gyro_yout / 131), gyro_zout, (gyro_zout / 131))
    # After retrieving MPU values
    database.child("GJ-10-AL-1998").child(road_uid).push({"x-accel": accel_xout,
                                          "y-accel": accel_yout,
                                          "z-accel": accel_zout,
                                          "x-gyro": gyro_xout,
                                          "y-gyro": gyro_yout,
                                          "z-gyro": gyro_zout,
                                          "x-accel_s": accel_xout/131,
                                          "y-accel_s": accel_yout/131,
                                          "z-accel_s": accel_zout/131,
                                          "x-gyro_s": gyro_xout/16384,
                                          "y-gyro_s": gyro_yout/16384,
                                          "z-gyro_s": gyro_zout/16384})
    print("x-accel:", accel_xout,"y-accel", accel_yout,"z-accel",  accel_zout,
          "x-gyro",  gyro_xout,"y-gyro",  gyro_yout,"z-gyro",  gyro_zout,
          "x-accel_s",  accel_xout/131,"y-accel_s",  accel_yout/131,
          "z-accel_s",  accel_zout/131,"x-gyro_s",  gyro_xout/16384,
          "y-gyro_s",  gyro_yout/16384,"z-gyro_s",  gyro_zout/16384)    



#accel_xout_scaled = accel_xout / 16384.0
#accel_yout_scaled = accel_yout / 16384.0
#accel_zout_scaled = accel_zout / 16384.0

#print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
#print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
#print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

#print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
#print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
