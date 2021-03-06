#!/usr/bin/env python3

import pdb
import sys
import serial
import time
from   hexdump   import hd
#from   threading import Thread

class channel():
    global b
    def __init__(self, port='/dev/ttyUSB1', baud=115200):
        print("Opening channel: {}, baud: {}".format(port, baud))
#        self.serial = serial.Serial(port, baud)
        self.serial = serial.serial_for_url(port, baud)
        self.pktnum=0
        self.zeroTime()
        self.serial.flushInput()
        self.timeout = 10/int(baud)*2

    def zeroTime(self):
        self.zeroTime = time.time()
        self.recvTime = self.zeroTime;
        print('\nzeroTime: {:f}'.format(self.zeroTime))

    def flush(self):
        self.serial.flushInput()

    def get_packet(self):
        b = b''
        cnt = 0
        self.recvTime = time.time()
        num = self.serial.inWaiting()
        if num > 0:
            b = self.serial.read(num)
            cnt = num
#            print("started with {} bytes".format(cnt))
        else:
            self.serial.timeout = None;
            b = self.serial.read(1)
            self.recvTime = time.time()
            cnt = 1

        self.serial.timeout = self.timeout
        while True:
            n = self.serial.read(63)
#            print("read {} bytes".format(len(n)))
            if n:
                b = b + n
                cnt += len(n)
                if cnt < 64:
                    continue
            break

        self.pktnum += 1
        return self.pktnum, self.recvTime, b

    def dump_packet(self, num, time, p):
        print('\npkt {:2d}: ({:2d})  {:f}'.format(num, len(p), time-self.zeroTime))
        print(hd(p), end="")

    def write(self, buf):
        self.serial.write(buf)

#def send_em(c):
#    n = 1
#    print("send_em start up")
#    print("sending pkt {}".format(n))
#    b = bytes.fromhex('00010203040506070809')
#    c.write(chr(n).encode())
#    time.sleep(.0001)
#    c.write(bytes.fromhex('999897'))
#    time.sleep(.0001)
#    c.write(b)
#    time.sleep(2)
#
#    n += 1
#    print("sending pkt {}".format(n))
#    c.write(chr(n).encode())
#    c.write(b)
#    time.sleep(.0001)
#    n += 1
#    print("sending pkt {}".format(n))
#    c.write(chr(n).encode())
#    c.write(b)
#    time.sleep(.0001)
#    n += 1
#    print("sending pkt {}".format(n))
#    c.write(chr(n).encode())
#    c.write(b)
#    time.sleep(.0001)
#    n += 1
#    print("sending pkt {}".format(n))
#    c.write(chr(n).encode())
#    c.write(b)

#chnl = channel('loop://', 115200)
#t = Thread(target=send_em, args=(chnl,))
#t.start()

''' Usage: serlook.py [serial port [baud]]

    if 1 parameter (no parameters), default to /dev/ttyUSB1 115200
    if 2 parameters (1 parameter),  <port> is supplied, default to 115200
    if >2, both port and baud supplied.
'''

if len(sys.argv) == 1:
    chnl = channel()
elif len(sys.argv) == 2:
    chnl = channel(sys.argv[1])
else:
    chnl = channel(sys.argv[1], sys.argv[2])

while True:
    pn, t, p = chnl.get_packet()
    chnl.dump_packet(pn, t, p)
