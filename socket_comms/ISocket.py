from __future__ import annotations

import abc
import selectors
import socket
from typing import TYPE_CHECKING

from .Buffer import Buffer
from .WrappedSelector import WrappedSelector

if TYPE_CHECKING:
    from .SocketConfig import SocketConfig


class ISocket(abc.ABC):
    """
    Socket interface.
    """

    def __init__(
        self,
        config: SocketConfig,
    ):
        # addressing
        self._address = config.address

        # buffer settings
        self._write_buffer = Buffer(config)
        self._buffer_size = config.buffer_size
        self._encoding = config.encode_format

        # socket/selector
        self._socket: socket.SocketType = socket.socket(
            config.address_family, config.socket_type
        )
        self._blocking = config.blocking
        self._selector = WrappedSelector()
        self._timeout = config.timeout_in_s

        # for debugging
        self._verbose = config.verbose

    def __del__(self):
        self._print("Closing socket.")
        self._selector.unregister(self._socket)
        self._socket.close()
        self._selector.close()

    def start(self):
        """
        Begins the main event loop. Events are detected by the selector.
        """
        while True:
            if self._selector.sockets:
                events = self._selector.select(timeout=self._timeout)

                for event in events:
                    self._handle_event(*event)

    @abc.abstractmethod
    def _handle_event(self, connection_key: selectors.SelectorKey, event_mask: int):
        """
        Different handling of events depending on whether self._socket
        is a server socket (listener) or a client socket.
        """
        raise NotImplementedError

    def _read_and_write(self, connection: socket.SocketType, event_mask: int):
        """
        Executes read event, followed by write event.
        """
        if event_mask & selectors.EVENT_READ:
            message = self.read(connection)

            if message:
                self._print(f"Received {message}")
            else:
                self._close_connection(connection)

        if event_mask & selectors.EVENT_WRITE:
            self.write(connection)

    def read(self, connection: socket.SocketType) -> str:
        """
        Returns data from connection during a read event.
        """
        try:
            connection.setblocking(self._blocking)
            received_bytes = connection.recv(self._buffer_size)
            message = received_bytes.decode(self._encoding)
        except ConnectionResetError as e:
            message = None
            print(e)
        return message

    def write(self, connection: socket.SocketType):
        """Sends the next portion of the write buffer to the server."""
        partial_bytes = next(self._write_buffer)

        if partial_bytes:
            connection.send(partial_bytes)
            print(f"Sending {partial_bytes.decode(self._encoding)}")

    def _close_connection(self, connection: socket.SocketType):
        """
        Deregisters client socket from the selector and closes it.
        """
        self._print(f"Closing connection at {connection.getpeername()}...")
        self._selector.unregister(connection)
        connection.close()

    def _print(self, text: str):
        """
        Prints text if verbose setting is set to True.
        """
        if self._verbose:
            print(text)
