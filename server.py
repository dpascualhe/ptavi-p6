#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys

# Comprobamos si los argumentos son válidos
if len(sys.argv) != 4:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
"""
elif sys.argv[4] does not exist:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
"""

# Puerto en el que escuchamos
PORT = int(sys.argv[2])

# Métodos que entendemos
accepted = ['INVITE', 'ACK', 'BYE']

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        line = self.rfile.read()
        print "El cliente nos manda " + line
        word = line.split(' ')

        # Envia los códigos de respuesta correspondientes
        if word[0] in accepted and word[2] == 'SIP/2.0\r\n\r\n':
            respuesta = "SIP/2.0 100 Trying\r\n\r\nSIP/2.0 180 Ring\r\n\r\nSIP/2.0 200 OK\r\n\r\n"
            self.wfile.write(respuesta)

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
