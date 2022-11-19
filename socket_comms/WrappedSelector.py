from selectors import DefaultSelector


class WrappedSelector(DefaultSelector):
    """
    Wrapper to expose select attributes from DefaultSelector.
    """

    @property
    def writers(self) -> list:
        """Returns a list of the stored writers."""
        return list(self._writers)

    @property
    def sockets(self) -> set:
        """Returns the registered sockets."""
        return self._readers | self._writers
