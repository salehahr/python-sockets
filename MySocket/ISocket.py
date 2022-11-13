from __future__ import annotations

import abc
import selectors
import socket
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MySocket import SocketConfig


def enable_quitting(func: callable) -> callable:
    def wrapped_function(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except KeyboardInterrupt:
            self._print("CTRL+C pressed. Quitting...")

    return wrapped_function


class ISocket(abc.ABC):
    """
    Socket interface.
    """

    def __init__(
        self,
        config: SocketConfig,
    ):
        self._host = config.host
        self._port = config.port
        self._blocking = config.blocking
        self._buffer_size = config.buffer_size

        self._socket: socket.SocketType = socket.socket(
            config.address_family, config.socket_type
        )
        self._selector = selectors.DefaultSelector()

        self._verbose = config.verbose

    def __del__(self):
        self._print("Closing socket.")
        self._socket.close()

    @enable_quitting
    def start(self):
        self._connect()

    @abc.abstractmethod
    def _connect(self):
        pass

    def _print(self, text: str):
        """
        Prints text if verbose setting is set to True.
        """
        if self._verbose:
            print(text)
