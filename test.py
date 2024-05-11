#!/usr/bin/env python

import aprslib
import qrzlib

qrz = qrzlib.QRZ()
qrz.authenticate("ON3URE", "")


def callback(packet):
    data = aprslib.parse(packet)

    call = data["from"]
    print(call)
    try:
        voltage = data["telemetry"]["vals"][1]

        try:
            qrzcall = call.split("-", 1)[0]
            print(qrzcall)
            qrz.get_call(qrzcall)
            print(qrz.fullname, qrz.zip, qrz.latlon, qrz.grid, qrz.email)
            print(voltage)
            if 1000 <= voltage <= 1200:
                print("Voltage is getting low!")

        except qrz.NotFound as err:
            print(err)
    except KeyError as err:
        print(err)


AIS = aprslib.IS("ON6URE")
AIS.set_login("ON6URE", "22716")
AIS.set_server("rotate.aprs2.net", 14580)
AIS.set_filter("u/APRFGT")
AIS.connect()
# by default `raw` is False, then each line is ran through aprslib.parse()
AIS.consumer(callback, raw=True)
