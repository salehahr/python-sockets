from dataclasses import dataclass
from typing import Optional


@dataclass
class SocketConfig:
    host: str
    port: int

    address_family: int
    socket_type: int

    buffer_size: int
    encode_format: str
    timeout_in_s: Optional[float]

    verbose: bool = False
    blocking: bool = False

    @property
    def address(self) -> tuple[str, int]:
        return self.host, self.port
