import socket

from MySocket import SocketConfig

HOST = "127.0.0.1"
PORT = 65432
ADDRESS_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
BUFFER_SIZE = 1024

socket_config = SocketConfig(
    host=HOST,
    port=PORT,
    address_family=ADDRESS_FAMILY,
    socket_type=SOCKET_TYPE,
    buffer_size=BUFFER_SIZE,
    verbose=True,
    blocking=False,
)
