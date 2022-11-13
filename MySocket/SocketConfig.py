from dataclasses import dataclass


@dataclass
class SocketConfig:
    host: str
    port: int
    buffer_size: int
    address_family: int
    socket_type: int
    verbose: bool = False
    blocking: bool = False
