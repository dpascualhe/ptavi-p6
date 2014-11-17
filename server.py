#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os

# Comprobamos si los argumentos son válidos
try: 
    audio = open (sys.argv[3], 'r')
    if len(sys.argv) != 4:
        raise IOError
except IOError:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit

print 'Listening...'
"""
elif sys.argv[4] does not exist:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
"""

# Puerto en el que escuchamos
PORT = int(sys.argv[2])

# Métodos que entendemos
accepted = ['INVITE', 'ACK', 'BYE']

# Damos permisos de ejecución al programa RTP
os.system("chmod +x mp32rtp")

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        line = self.rfile.read()

        # Envia los códigos de respuesta correspondientes
        while 1:      
            print "El cliente nos manda " + line
            word = line.split(' ')
            if word[0] in accepted and word[2] == 'SIP/2.0\r\n\r\n':
                respuesta = "SIP/2.0 100 Trying\r\n\r\nSIP/2.0 180 Ring\r\n\r\n"
                respuesta += "SIP/2.0 200 OK\r\n\r\n"
            elif not word[0] in accepted:
                respuesta = "SIP/2.0 405 Method Not Allowed"
            else:
                respuesta = "SIP/2.0 400 Bad Request"
                
            self.wfile.write(respuesta)
            line = self.rfile.read()
            if not line:
                break        
        
        rtp_send = "./mp32rtp -i 127.0.0.1 -p 23032 < " + sys.argv[3]
        print "Vamos a ejecutar", rtp_send
        os.system (rtp_send)
        

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
