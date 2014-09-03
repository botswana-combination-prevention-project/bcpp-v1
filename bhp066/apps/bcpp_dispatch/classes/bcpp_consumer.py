from edc.device.sync.classes import Consumer

from .bcpp_signal_manager import BcppSignalManager


class BcppConsumer(Consumer, BcppSignalManager):

    def disconnect_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        self._disconnect_bcpp_signals()

    def reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        self._reconnect_bcpp_signals()
