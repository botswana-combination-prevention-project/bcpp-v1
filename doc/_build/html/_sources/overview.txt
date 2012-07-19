Overview
========

Provide a consistent method to determine the device id used by applications such as :mod:`bhp_identifier`.


:usage:
    >>> device = Device()
    >>> device.device_id
    >>> 31

:class:`~bhp_device.classes.device.Device` :attr:`device_id` is set with the current device id. It can determine the 
device_id from the :file:`settings.py`, using the :py:mod:`socket` method :py:func:`socket.gethostname` along with the settings
attribute HOSTNAME_PREFIX, or via the :mod:`bhp_variables` model values.
