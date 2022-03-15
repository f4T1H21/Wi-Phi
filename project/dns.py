# ﺏ
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
# ATTENTION:
# All additional methods of the class 'UDPServer' is removed as an ethical precaution.
# Without these methods, the software won't work properly.
#
# 'DNSQuery class' is licensed under the Apache License, Version 2.0 (the "Class's License").
# You may not use this class except in compliance with the Class's License.
# You may obtain a copy of the Class's License at
#
# http://www.apache.org/licenses/LICENSE-2.0

import gc
import sys
import socket
import _thread

class DNSQuery:
    def __init__(self, data:bytes):
        self.data = data
        self.domain = ''
        tipo = (data[2] >> 3) & 15  # Opcode bits
        if tipo == 0:               # Standard query
            ini = 12
            lon = data[ini]
            while lon != 0:
                self.domain += data[ini + 1:ini + lon + 1].decode('utf-8') + '.'
                ini += lon + 1
                lon = data[ini]
            self.domain = self.domain[:-1]


    def answer(self, ip:str) -> bytes:
        if self.domain:
            packet  = self.data[:2] + b'\x81\x80'
            packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'   # Questions and Answers Counts
            packet += self.data[12:]                                          # Original Domain Name Question
            packet += b'\xC0\x0C'                                             # Pointer to domain name
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3C\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
            packet +=  bytes(map(int, ip.split('.')))                         # 4bytes of IP
        return packet


class UDPServer:
    def __init__(self, host:str, port:int=53):
        self.host = host
        self.accepted_domains = {
                'ncsi', 'msftconnecttest', 'connectivitycheck', 'clients3', 'detectportal',
                'google', 'login', 'gvt2', 'gvt3', 'apple', 'connect', 'miui'
            }
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind((host, port))
        print(f'[DNS] Server listening on {host}:{port}/udp')

        _thread.start_new_thread(self.DNSServer, ())