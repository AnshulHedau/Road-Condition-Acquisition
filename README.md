# Road-Condition-Acquisition
Data acquisition on the condition of roads with the use of Raspberry Pi. This is a part of two-part project, have a look at the data analysis module here: https://github.com/Dheeraj1998/Road-Condition-Analysis

# Interfacing Raspberry Pi and MPU-6050

## How to Setup the device (Rasbian OS)

It's an I<sup>2</sup>C board so first you need to install the relevant Linux drivers.
* **Open the file for editing** (needs sudo)
> sudo vi /etc/modules 

* **Add the following lines to the bottom of the file, save it and reboot the Pi**
> i2c-bcm2708 <br>
> i2c-dev

* **Now check the blacklists file**
> sudo vi /etc/modprobe.d/raspi-blacklist.conf

* **Make sure that the following lines if present start with a # (Lines are commented) , if not nothing to worry**
> #blacklist spi-bcm2708 <br>
> #blacklist i2c-bcm2708

## Connecting the Sensor

We will make use of GPIO pins to make the connections with Pi
The pins to be connected are
* **Pin 1** - 3.3V connect to VCC
* **Pin 3** - SDA connect to SDA
* **Pin 5** - SCL connect to SCL
* **Pin 6** - Ground connect to GND

## Verifing the Connections

For testing if the Pi has detcted the board connected. Following copmmands are used to install the i2c tools

*   **Step 1**
>   sudo apt-get install i2c-tools

*   **Step 2** (For Revision 1 board) 
>   sudo i2cdetect -y 0 <br>

*   **Step 2** (For Revision 2 board)
>   sudo i2cdetect -y 1 <br>

### We need to install the smbus module to read from the I2C using Python bus 
* **Installation Command**
> sudo apt-get install python-smbus 

## Congrats, we are done!
Now execute the above code to check if we are getting the correct data.
