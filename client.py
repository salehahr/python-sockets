from __future__ import annotations

from typing import TYPE_CHECKING

from config import socket_config
from socket_comms import ClientSocket

if TYPE_CHECKING:
    from socket import SocketType


class UserInputClient(ClientSocket):
    """
    Client that takes user input and sends it to a server.
    """

    def write(self, connection: SocketType):
        """
        Appends the user input to the write buffer and sends it to the server.
        """
        self._write_buffer += input("Type message: ")
        super(UserInputClient, self).write(connection)


client = UserInputClient(socket_config)
client.start()
