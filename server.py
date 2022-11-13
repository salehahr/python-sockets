from config import socket_config
from MySocket import ServerSocket

server = ServerSocket(socket_config)
server.start()
