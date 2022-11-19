from __future__ import annotations

from typing import TYPE_CHECKING

from config import socket_config
from socket_comms import ServerSocket

if TYPE_CHECKING:
    from socket import SocketType


class EchoServer(ServerSocket):
    """
    Server that reads messages from the client and sends them back.
    """

    def read(self, connection: SocketType) -> str:
        """
        Reads data from connection during a read event.
        Adds data to the write buffer to be echoed back to
        the client.
        """
        message = super(EchoServer, self).read(connection)
        self._write_buffer += message
        return message


server = EchoServer(socket_config)
server.start()
