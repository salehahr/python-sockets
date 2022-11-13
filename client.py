from config import socket_config
from MySocket import ClientSocket

client_socket = ClientSocket(socket_config)
client_socket.start()

client_socket.send(b"Hello from the client!")
