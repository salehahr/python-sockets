from __future__ import annotations

import selectors
from typing import TYPE_CHECKING

from .ISocket import ISocket

if TYPE_CHECKING:
    from .SocketConfig import SocketConfig


class ClientSocket(ISocket):
    """
    Socket that acts a client in a server-client communication process.
    """

    def __init__(self, config: SocketConfig):
        super(ClientSocket, self).__init__(config)

        self._connect()

    def _connect(self):
        self._socket.connect(self._address)
        self._print(f"Connecting to host: {self._address}")

        self._selector.register(
            self._socket, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None
        )

    def _handle_event(self, connection_key: selectors.SelectorKey, event_mask: int):
        """
        Proceeds directly with read and write operations.
        """
        connection = connection_key.fileobj
        self._read_and_write(connection, event_mask)
