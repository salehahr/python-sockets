from __future__ import annotations

import selectors
import socket
import types
from typing import TYPE_CHECKING

from .ISocket import ISocket

if TYPE_CHECKING:
    from .SocketConfig import SocketConfig

EVENTS_READ_WRITE = selectors.EVENT_READ | selectors.EVENT_WRITE


def base_data(address: int) -> types.SimpleNamespace:
    return types.SimpleNamespace(address=address, inb=b"", outb=b"")


def make_selector_key(socket_: socket.SocketType) -> selectors.SelectorKey:
    return selectors.SelectorKey(
        socket_,
        fd=socket_.fileno(),
        events=EVENTS_READ_WRITE,
        data=base_data(socket_.getpeername()),
    )


class ServerSocket(ISocket):
    def __init__(self, config: SocketConfig):
        super(ServerSocket, self).__init__(config)

        self._client_counter = 0
        self._selector_timeout = None if self._blocking else 0

        self._listen()

    def _listen(self):
        """
        Sets up listener socket, registers it with the selector.
        """
        self._socket.bind((self._host, self._port))
        self._socket.listen()

        if not self._blocking:
            self._socket.setblocking(False)

        self._selector.register(self._socket, selectors.EVENT_READ, data=None)

        self._print(f"Listening on {self._host}:{self._port}")

    def __del__(self):
        self._selector.unregister(self._socket)
        super(ServerSocket, self).__del__()

    def _connect(self):
        """
        Listener socket accepts new connections.
        Once accepted, client sockets are created and handled
        according to event type.
        """
        while True:
            socket_events = self._selector.select(timeout=self._selector_timeout)
            for event in socket_events:
                self._handle_event(*event)

    def _handle_event(self, client: selectors.SelectorKey, event_mask):
        """
        Create new client socket, read data, or write data according
        to event type.
        :param client:
        :param mask:
        :return:
        """
        if client.data is None:
            client = self._new_client_socket()

        self._read_or_write(client, event_mask)

    def _new_client_socket(self) -> selectors.SelectorKey:
        """
        Accepts connection request in form of a client socket
        and registers it to the selector.
        :return: client key object containing the socket
        """
        client, _ = self._socket.accept()
        client.setblocking(False)

        client_key = make_selector_key(client)
        self._register_client(client_key)

        return client_key

    def _read_or_write(self, client: selectors.SelectorKey, event_mask: int):
        if event_mask == selectors.EVENT_READ:
            self._read(client)
        # elif event_mask == selectors.EVENT_WRITE:
        #     self._write(client)
        else:
            self._deregister_client(client)

    # --- reading functionality
    def _read(self, client_key: selectors.SelectorKey):
        """
        Reads data from client socket during a read event.
        If no data is received, deregisters the socket from selector.
        """
        self._print("Reading...")
        received_data = self._receive(client_key.fileobj)

        if received_data:
            data = client_key.data.outb + received_data
            print(f"Received: {data.decode('ascii')}")
        else:
            # no data received indicates end of read event
            self._deregister_client(client_key)

    def _receive(self, client: socket.SocketType) -> optional[bytes]:
        """
        Handles data reception from client socket.
        """
        try:
            received_data = client.recv(self._buffer_size)
        except OSError as e:
            received_data = None
            self._print("Error: client socket already closed.")
            self._print(str(e))

        return received_data

    # --- selector registering/deregistering
    def _register_client(self, client_key: selectors.SelectorKey):
        """
        Registers client socket to the selector.
        """
        self._print(f"Registering connection from {client_key.data.address}")
        self._increment_counter()

        self._selector.register(
            client_key.fileobj, EVENTS_READ_WRITE, data=client_key.data
        )

    def _deregister_client(self, client_key: selectors.SelectorKey):
        """
        Deregisters client socket from the selector and closes it.
        """
        self._print(f"Unregistering connection to {client_key.data.address}")
        self._decrement_counter()

        client = client_key.fileobj
        self._selector.unregister(client)
        client.close()

    # --- counter functionality
    def _increment_counter(self):
        self._client_counter += 1
        self._print_counter()

    def _decrement_counter(self):
        self._client_counter -= 1
        self._print_counter()

    def _print_counter(self):
        """Prints number of connected clients."""
        self._print(f"Clients: {self._client_counter}")
