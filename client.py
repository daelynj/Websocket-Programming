from socket import *
import sys

server_host = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.connect((server_host, int(server_port)))

    try:
        server_socket.send(('GET /' + filename).encode())
        message = server_socket.recv(1024)

        while message:
            print(message.decode())
            message = server_socket.recv(1024)
        
        server_socket.close()
    except IOError:
        server_socket.send(b'\nHTTP/1.1 404 Not Found\n\n')
        server_socket.close()