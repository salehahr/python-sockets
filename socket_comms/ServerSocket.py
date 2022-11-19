from __future__ import annotations

import selectors
from typing import TYPE_CHECKING

from .ISocket import ISocket

if TYPE_CHECKING:
    from .SocketConfig import SocketConfig


class ServerSocket(ISocket):
    """
    Socket that acts a server in a server-client communication process.
    """

    def __init__(self, config: SocketConfig):
        super(ServerSocket, self).__init__(config)

        self._listen()

    def _listen(self):
        """
        Sets up listener socket, registers it with the selector.
        """
        self._selector.register(self._socket, selectors.EVENT_READ, data="NEW")

        self._socket.bind(self._address)
        self._socket.listen()

        self._print(f"Listening on {self._address}")

    def _handle_event(self, connection_key: selectors.SelectorKey, event_mask: int):
        """
        First checks for new connections to be registered to the selector.
        If no new connections are found, proceeds with read and write
        operations.
        """
        if connection_key.data == "NEW":
            self._accept_new_connection()
            return
        else:
            connection = connection_key.fileobj

        self._read_and_write(connection, event_mask)

    def _accept_new_connection(self):
        """
        Registers new connection to the selector.
        """
        connection, _ = self._socket.accept()
        self._selector.register(
            connection, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None
        )
        print(f"Connecting to {connection.getpeername()}...")

    def _check_connections(self):
        """
        Checks the connection status of all writable sockets.
        If a socket has been closed unexpectedly, removes this socket
        from the selector.
        """
        self._print("Checking connections...")

        for writer in self._selector.writers:
            client = self._selector.get_key(writer)
            if client.fileobj._closed:
                self._deregister_client(client)
