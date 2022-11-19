import socket

from socket_comms import SocketConfig

HOST = "127.0.0.1"
PORT = 65432
ADDRESS_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
BUFFER_SIZE_IN_BYTES = 4
TIMEOUT_IN_S = 0.5
ENCODE_FORMAT = "utf-8"

socket_config = SocketConfig(
    host=HOST,
    port=PORT,
    address_family=ADDRESS_FAMILY,
    socket_type=SOCKET_TYPE,
    buffer_size=BUFFER_SIZE_IN_BYTES,
    encode_format=ENCODE_FORMAT,
    timeout_in_s=TIMEOUT_IN_S,
    verbose=True,
    blocking=False,
)
