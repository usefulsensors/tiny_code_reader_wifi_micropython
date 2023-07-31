# Tiny Code Reader Wifi Provisioning on a Pico W
Example of using the Tiny Code Reader to set the wifi name and password from MicroPython on a Pico W.

The [Tiny Code Reader](https://usfl.ink/tcr) from [Useful Sensors](https://usefulsensors.com)
is a small hardware module that's intended to make it easy
to scan QR codes. It has an image sensor and a microcontroller with pretrained
software and outputs information from any identified codes over I2C.

It is designed to be used as an input to a larger system, and this example
shows how to read it from a Raspberry Pi Pico W using MicroPython, and set up
the Wifi name and password. It can also be used as the starting point for other
MicroPython-based boards, but since the exact syntax used to access the I2C bus
varies across platforms, you'll probably need to modify the lines that mention
`i2c` in the main Python script. For a full developer's guide, see [usfl.ink/tcr_dev](https://usfl.ink/tcr_dev).

## Setting up MicroPython

You should read the [official guide to setting up MicroPython on a Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
for the latest information, but here is a summary:

 - Download MicroPython for the for your board from micropython.org. For
 example the Pico version is available at [micropython.org/download/rp2-pico-w/](https://micropython.org/download/rp2-pico-w/).
 This project has been tested using the `1.20.0` version.
 - Hold down the `bootsel` button on the Pico and plug it into a USB port.
 - Drag the MicroPython uf2 file onto the `RPI-RP2` drive that appears.

I recommend downloading [Thonny](https://thonny.org/) to your desktop computer
to run the MicroPython script. If you see a runtime error that `import network`
has failed, then it's likely you've used the **Pico** version of MicroPython, 
not the Pico **W**.

## Wiring Information

Wiring up the device requires 4 jumpers, to connect VDD, GND, SDA and SCL. The 
example here uses I2C port 0, which is assigned to GPIO4 (SDA, pin 6) and GPIO5
(SCL, pin 7) in software. Power is supplied from 3V3(OUT) (pin 36), with ground
attached to GND (pin 38).

Follow the wiring scheme shown below:

![Wiring diagram for Person Sensor/Pico](pico_person_sensor_bb.png)

If you're using [Qwiic connectors](https://www.sparkfun.com/qwiic), the colors 
will be black for GND, red for 3.3V, blue for SDA, and yellow for SDC.

## Running the program

Open up Thonny, paste the contents of `main.py` into a new file and save it
on the Pico W as `main.py`. Press the run button.

It will start by entering a loop that looks for a QR code containing Wifi 
network information. On Android [you can just go to Wifi settings, choose share](https://www.theverge.com/23561652/android-ios-wifi-password-share-how-to),
and it will display a code containing the name and password of the network
you're currently connected to. [It's also possible to do the same thing on iOS](https://osxdaily.com/2021/07/08/how-share-wi-fi-password-qr-code-shortcuts/)
but it's a bit more fiddly.

Once you have the QR code on your phone screen, show it to the Tiny Code Reader.
The best distance is between four to six inches (ten to fifteen centimetres)
from the sensor, and you may need to wiggle it a little to get a good read.

After it has read the network name and password it will print "Connecting" to
the serial console, and then hopefully connect to the Wifi and print out its
IP information.

## Troubleshooting

### Power

The first thing to check is that the sensor is receiving power through the
`VDD` and `GND` wires. The simplest way to test this is to look at the LED on
the front of the module. Whenever it has power, it should be flashing blue
multiple times a second. If this isn't happening then there's likely to be a
wiring issue with the power connections.

### Communication

If you see connection errors when running the code detection example, you may
have an issue with your wiring. To help track down what's going wrong, you can
uncomment the `i2.scan()` line in the script.

This will display which I2C devices are available in the logs. You want to make
sure that address number `12` is present, because that's the one used by the
person sensor. Here's an example from a board that's working:

```bash
[12]  
```

You can see that `12` is shown. If it isn't present then it means the sensor
isn't responding to I2C messages as it should be. The most likely cause is that 
there's a wiring problem, so if you hit this you should double-check that the 
SDA and SCL wires are going to the right pins.

## Going Further

This script is designed to show you the basics of Wifi provisioning with a QR
code reader. In a real application you'll probably want to only do this once
at initialization time and then [store the results persistently](https://electrocredible.com/rpi-pico-save-data-permanently-flash-micropython/)
so the user doesn't have to do this every time the device reboots.