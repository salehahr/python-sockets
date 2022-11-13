from __future__ import annotations

from typing import TYPE_CHECKING

from .ISocket import ISocket

if TYPE_CHECKING:
    import SocketConfig


class ClientSocket(ISocket):
    def __init__(self, config: SocketConfig):
        super(ClientSocket, self).__init__(config)

    def _connect(self):
        self._socket.connect((self._host, self._port))
        self._print(f"Connecting to {self._host}:{self._port}")

    def send(self, data: bytes):
        self._socket.sendall(data)

    def receive(self):
        data = self._socket.recv(self._buffer_size)
        self._print(f"Received data from server: {data.decode('ascii')}")
