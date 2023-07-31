import network
import struct
from time import sleep
import machine

# The code reader has the I2C ID of hex 0c, or decimal 12.
TINY_CODE_READER_I2C_ADDRESS = 0x0C

# How long to pause between sensor polls.
TINY_CODE_READER_DELAY = 0.05

TINY_CODE_READER_LENGTH_OFFSET = 0
TINY_CODE_READER_LENGTH_FORMAT = "H"
TINY_CODE_READER_MESSAGE_OFFSET = TINY_CODE_READER_LENGTH_OFFSET + struct.calcsize(TINY_CODE_READER_LENGTH_FORMAT)
TINY_CODE_READER_MESSAGE_SIZE = 254
TINY_CODE_READER_MESSAGE_FORMAT = "B" * TINY_CODE_READER_MESSAGE_SIZE
TINY_CODE_READER_I2C_FORMAT = TINY_CODE_READER_LENGTH_FORMAT + TINY_CODE_READER_MESSAGE_FORMAT
TINY_CODE_READER_I2C_BYTE_COUNT = struct.calcsize(TINY_CODE_READER_I2C_FORMAT)

# Set up for the Pico, pin numbers will vary across boards.
i2c = machine.I2C(0,
                  scl=machine.Pin(5),
                  sda=machine.Pin(4),
                  freq=400000)

def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    return wlan

# Uncomment this to see what peripherals were detected on the bus. We would
# expect to see [12] as the output, since that's the sensor's ID.
# print(i2c.scan())

# Keep looping and reading the person sensor results until we get a wifi QR
# code that lets us connect.
while True:
    sleep(TINY_CODE_READER_DELAY)
    read_data = i2c.readfrom(TINY_CODE_READER_I2C_ADDRESS,
                             TINY_CODE_READER_I2C_BYTE_COUNT)

    message_length,  = struct.unpack_from(TINY_CODE_READER_LENGTH_FORMAT, read_data, TINY_CODE_READER_LENGTH_OFFSET)
    message_bytes = struct.unpack_from(TINY_CODE_READER_MESSAGE_FORMAT, read_data, TINY_CODE_READER_MESSAGE_OFFSET)

    if message_length == 0:
        continue
    try:
        message_string = bytearray(message_bytes[0:message_length]).decode("utf-8")
        # Example wifi provisioning text:
        # WIFI:S:useful_sensors;T:WPA;P:somepassword;H:false;;
        if message_string.startswith("WIFI:"):
            message_parts = message_string[5:].split(";")
            wifi_ssid = None
            wifi_password = None
            for part in message_parts:
                if part == "":
                    continue
                key, value = part.split(":")
                if key == "S":
                    wifi_ssid = value
                elif key == "P":
                    wifi_password = value
            wlan = connect(wifi_ssid, wifi_password)
            if wlan.isconnected():
                break
        else:
            print("Couldn't interpret '%s' as a wifi network name and password" % message_string)
    except:
        print("Couldn't decode as UTF 8")
        pass

# Now we're connected, do something with the network.
print("Connected!")
print(wlan.ifconfig())