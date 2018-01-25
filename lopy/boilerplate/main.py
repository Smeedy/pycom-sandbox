from network import LoRa
import binascii
import socket
import time

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, adr=True, device_class=LoRa.CLASS_A, sf=7)

app_eui = binascii.unhexlify('some_app_hex')
dev_eui = binascii.unhexlify('some_dev_hex')
app_key = binascii.unhexlify('some_secret_hex')

# join a network using OTAA
print('** joining network')
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    print('OTAA: Not joined yet...')
    pycom.rgbled(0x552000) # orange

    time.sleep(0.05)
    pycom.rgbled(0x000000)
    time.sleep(1.5)

# we are connected!
print('OTAA: joined')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

i = 1
while True:

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    # sending binary
    # frame = bytearray()
    # frame.extend(b'\x01\x02') # raw
    # s.send(frame)

    # sensing string
    up = 'Hello world {}'.format(i)
    s.send(up)
    print('UP msg sent: {}'.format(up))

    # show the audience
    pycom.rgbled(0x002200) # green
    time.sleep(0.3)
    pycom.rgbled(0x000000)

    # make the socket non-blocking again
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    rx = s.recv(256)
    if rx:
        pycom.rgbled(0x220022) # purple
        time.sleep(4)
        pycom.rgbled(0x000000)
        print('** DOWN msg received:')
        print(rx)

    i += 1
    time.sleep(10)
