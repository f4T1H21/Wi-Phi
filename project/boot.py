# Copyright [2022] Şefik Efe Altınoluk
#
# This file is a part of project Wi-Phi©
# For more details, see https://github.com/f4T1H21/Wi-Phi
#
# Licensed under the GNU GENERAL PUBLIC LICENSE Version 3.0 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/gpl-3.0.html
#
# Memory (RAM) is overloaded when the server has to handle multiple
# clients requesting large resources (such as images) at the same time.
# In such a case, the IoT device (ESP32) may collapse.
# This problem can be solved by rebooting the device using onboard button.

import time
import random
import network
import _thread
import binascii
from server import TCPServer
from dns import UDPServer

# Generate a random MAC address (for anonymity) (vendor is 'Cisco Systems Inc.')
mac_bytes = (0x00, 0x07, 0x50, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff))
mac = ':'.join(map(lambda x: "%02x" % x, mac_bytes)).upper()
mac_encoded = binascii.unhexlify(''.join(i for i in mac.split(':')).encode())

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(mac=mac_encoded, essid=(essid:='Google Free Wi-Fi'), channel=11)
# Set IP address, subnet mask, gateway, DNS server respectively
ap.ifconfig(('210.210.210.1','255.255.255.0','210.210.210.1','210.210.210.1'))
my_ip = ap.ifconfig()[0]
print(f'[Wi-Fi] Wireless AP is active; ESSID = {essid}, BSSID = {mac}')

# Whenever a station connects to Wi-Fi (Wireless AP), print details.
def stations_status():
    indexed_sta = {}
    indexed_len = 0
    while True:
        current_sta = {binascii.hexlify(i[0], ':').decode().upper() for i in ap.status('stations')}
        current_len = len(current_sta)
        if current_len != indexed_len:
            if current_len > indexed_len:
                print('[Wi-Fi] Station(s) Connected: ' + ', '.join(current_sta - indexed_sta))
                print('[Wi-Fi] Current station status: '+ ', '.join(current_sta))
            if current_len < indexed_len:
                print('[Wi-Fi] Station(s) Disconnected: ' + ', '.join(indexed_sta - current_sta))
                print('[Wi-Fi] Current station status: '+ ', '.join(current_sta))
        indexed_sta = current_sta
        indexed_len = len(current_sta)
        time.sleep(.1)

_thread.start_new_thread(stations_status, ())
UDPServer(my_ip, 53)            # Start DNS server on a seperated thread.
TCPServer((my_ip, 80), 2121)    # Start Communication and HTTP servers.