#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


def raise_error():
    """ Procedimiento que eleva la excepcion """
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

# Comprobamos si tenemos los argumentos correctos
if len(sys.argv) != 3:
    raise_error()

# Dirección IP y puerto del servidor. Si hay algún error eleva la excepción
try:
    SERVER = sys.argv[2].split('@')[1].split(':')[0]
    PORT = int(sys.argv[2].split('@')[1].split(':')[1])
except ValueError:
    raise_error()
except IndexError:
    raise_error()

# Método requerido
METHOD = sys.argv[1]

PETICION = METHOD + " sip:" + sys.argv[2] + " SIP/2.0\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

# Enviamos la peticion
print "Enviando: " + PETICION
my_socket.send(PETICION + '\r\n')
try:
    data = my_socket.recv(1024)
except socket.error:
    print "Error: No server listening at " + SERVER + ":", PORT
    raise SystemExit

# Procesamos la respuesta
line = data.split('\r\n\r\n')[:-1]
ack = 0
if line == ["SIP/2.0 100 Trying", "SIP/2.0 180 Ring", "SIP/2.0 200 OK"]:
    # Si todo va bien enviamos un ACK
    respuesta = "ACK sip:" + sys.argv[2] + " SIP/2.0\r\n" + '\r\n'
    my_socket.send(respuesta)
    ack = 1
elif line == ["SIP/2.0 400 Bad Request"]:
    print "El servidor no entiende la petición"
elif line == ["SIP/2.0 405 Method Not Allowed"]:
    print "El servidor no entiende el método requerido"

print 'Recibido -- ', data
if ack:
    print 'Enviamos:' + respuesta
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
