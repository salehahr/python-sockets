from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .SocketConfig import SocketConfig


class Buffer:
    def __init__(self, config: SocketConfig):
        self._encoding = config.encode_format
        self._buffer_size = config.buffer_size

        self._data: optional[bytes] = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self._data:
            return None

        partial_message = self._data[: self._buffer_size]
        self._data = self._data[self._buffer_size :]

        return partial_message

    @property
    def data(self):
        if self._data:
            return self._data.decode(self._encoding)
        else:
            return None

    @data.setter
    def data(self, value: Union[str, bytes]):
        if isinstance(value, str):
            self._data = value.encode(self._encoding)
        elif isinstance(value, bytes):
            self._data = value
        elif value is None:
            self._data = None
        else:
            raise TypeError(
                f"Wrong data type -- got {type(value)} instead of str/bytes."
            )

    def __add__(self, other: str):
        if self._data:
            self.data += other
        else:
            self.data = other
        return self

    def __iadd__(self, other: str):
        return self.__add__(other)
