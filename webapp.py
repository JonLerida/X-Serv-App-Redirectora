#! /usr/bin/python3

""" X-Serv-App-Redirectora

Ejercicio de asignaturas de aplicaciones web. Servicios que interoperan. Aplicación redirectora.
Enunciado

Construir un programa en Python que sirva cualquier invocación que se le realice con una redirección
(códigos de resultado HTTP en el rango 3xx) a otro recurso (aleatorio) de si mismo.
"""

import socket
import random
import urllib.parse


class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        try:
            dest = request.split()[4]
        except ValueError:
            return None
        return dest


    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        newURL = 'http://'+parsedRequest+'/'+str(int(random.random() * 10000000))

        return ("307 Temporary Redirect", '<html><body><h1> Redireccionando...</h1><br>'+
                            '<p>Tu siguiente URL...' +newURL+
                            '<br>(mira la URL de arriba)</p>'+
                            '<meta http-equiv="Refresh" content="5;url='+ newURL+'"><br>'+
                            '</html>')

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        try:
            while True:
                print('Waiting for connections')
                (recvSocket, address) = mySocket.accept()
                print('HTTP request received (going to parse and process):')
                request = recvSocket.recv(2048).decode('utf-8')
                print(request)
                parsedRequest = self.parse(request)
                if parsedRequest == None:
                    returnCode = '404 Not Found'
                    htmlAnswer = '<html><h1>Error interno. Prueba "localhost:1234"</h1></html>'
                else:
                    (returnCode, htmlAnswer) = self.process(parsedRequest)
                print('Answering back...')
                recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                + htmlAnswer + "\r\n", 'utf-8'))
                recvSocket.close()
        except KeyboardInterrupt:
            print("Closing program")
            mySocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
