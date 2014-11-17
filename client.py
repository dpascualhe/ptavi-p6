#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Comprobamos si tenemos los argumentos correctos
if len(sys.argv) != 3:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

# Dirección IP del servidor.
SERVER = sys.argv[2].split('@')[1].split(':')[0]
PORT = int(sys.argv[2].split('@')[1].split(':')[1])

# Método requerido
METHOD = sys.argv[1]

PETICION = METHOD + " sip:" + sys.argv[2] + " SIP/2.0\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + PETICION
my_socket.send(PETICION + '\r\n')
try:
    data = my_socket.recv(1024)
except socket.error:
    print "Error: No server listening at 193.147.73.20 port 5555"
    raise SystemExit    

data = data.split('\r\n\r\n')

i = 0
"""mess = []
for line in data:
    mess.append(line)
    i += 1"""
"""
if mess = ["SIP/2.0 100 Trying", "SIP/2.0 180 Ring", "SIP/2.0 200 OK"]:
    my_socket.send("ACK sip:" + sys.argv[2] + " SIP/2.0\r\n" + '\r\n')
elif mess = ["SIP/2.0 400 Bad Request"]:
    print "El servidor no entiende la petición"
elif mess = ["SIP/2.0 405 Method Not Allowed"]:
    print "El servidor no entiende el método requerido"
"""
print data
if data == ["Hemos recibido tu peticion"]:
    PETICION = "ACK sip:" + sys.argv[2] + " SIP/2.0\r\n"
    my_socket.send(PETICION + '\r\n')
    print "Enviando: " + PETICION

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
