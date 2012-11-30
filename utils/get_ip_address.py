import socket
import fcntl
import struct


def get_ip_address(ifname):

    """
        from http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/

        >>> get_ip_address('lo')
        '127.0.0.1'

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])
    except IOError:
        ip = None

    return ip
