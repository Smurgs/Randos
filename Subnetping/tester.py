import socket
import fcntl
import struct

SIOCGIFNETMASK = 0x891b

def get_network_mask(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    netmask = fcntl.ioctl(s, SIOCGIFNETMASK, struct.pack('256s', str.encode(ifname)))[20:24]
    return socket.inet_ntoa(netmask)

get_network_mask("en0")