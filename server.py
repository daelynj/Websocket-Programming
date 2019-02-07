from socket import *
import sys

#Prepare a server socket
#host can be a hostname, IP address, or empty string. this is the standard ip address for the loopback interface
#if you pass an empty string to host, all connects will be accepted on all available ipv4 interfaces
#HOST = '' does this need to be specified?
port = 1234

#p1 indicates the ipv4 address family, p2 indicates the socket type, TCP
with socket(AF_INET, SOCK_STREAM) as server_socket:
    print('socket successfully created')

    #because we are using ipv4, bind expects a 2-tuple
    #bind() is used to associate the socket with a specific network interface and port number
    server_socket.bind(('', port))
    print('socket bound to', port)

    #.listen() specifies the number of unaccepted connections that the system will allow before refusing new connections
    #parameter is optional. if not specified, a default backlog value is chosen
    server_socket.listen(1)
    print('socket listening')

    while True:
        #accept() blocks and waits for an incoming connection. 
        #When a client connects, it returns a new socket object representing the connection and a tuple holding the address of the client. 
        #The tuple will contain (host, port) for IPv4
        connection_socket, addr =  server_socket.accept()
        print('connection established from', addr)

        """
        it's important to note that we are now using a different socket, con_soc will be used to communicate with the client
        whereas serv_soc is used to listen
        """

        try:
            message = connection_socket.recv(1024)

            #filename = message.split()[0] use 0 if testing through telnet
            filename = message.split()[1]
            print('data received:', filename[1:].decode())

            f = open(filename[1:])
            output_data = f.read()

            connection_socket.send(b'\nHTTP/1.1 200 OK\n\n')
            connection_socket.send(output_data.encode())  #use this when testing in the browser

            #do i even need this? why was it provided.
            #Send the content of the requested file to the client
            """for i in range(0, len(output_data)):           
                connection_socket.send(output_data[i].encode())
            connection_socket.send("\r\n".encode())"""

            connection_socket.close()
        except IOError:
            #Send response message for file not found
            connection_socket.send(b'\nHTTP/1.1 404 Not Found\n\n')
            connection_socket.close()