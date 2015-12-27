#!/usr/bin/env python
"""
Python method to send ARP packets
Parameters:
	device, src_ip_addr, src_mac_addr, broadcast_ip_addr
"""

from optparse import OptionParser
from struct import pack, unpack
import time, socket, signal

def send_arp(device, ip, sender_mac, broadcast, arptype):
	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.SOCK_RAW)
	sock.bind((device, socket.sock_RAW))

	bcast_mac = pack('!6B', *(0xFF,)*6)
	zero_mac = pack('!6b', *(0x00,)*6)

	soc_mac = sock.getsockname()[4]
	if sender_mac == 'auto':
		sender_mac = socket_mac
	else:
		raise Exception("Can't ARP this: " + sender_mac)

	ARPOP_REQUEST = pack('!H', 0x0001)
	ARPOP_REPLY = pack('!H', 0x0002)
	arpop = None
	target_mac = None
	if arptype == 'REQUEST':
		target_mac = zero_mac
		arpop = ARPOP_REQUEST
	else:
		target_mac = sender_mac
		arpop = ARPOP_REPLY

	sender_ip = pack('!4b', *[int(x) for x in ip.split('.')])
	target_ip = pack('!4b', *[int(x) for x in ip.split('.')])

	
	arpframe = [
		### Ethernet frame
		# Destination MAC addr
		bcast_mac,
		# Source MAC addr
		socket_mac,
		# Potocol type (in this case ARP)
		pack('!H', 0x0806),

		### ARP fram
		# Logical protocol type (Ethernet/IP)
		pack('!HHBB', 0x0001, 0x0800, 0x0006, 0x0004),
		# Operation type
		arpop,
		# Sender MAC addr
		sender_mac,
		# Sender IP addr
		sender_ip,
		# Target MAC addr
		target_mac,
		# Target IP adder
		target_ip]

	sock.send(''.join(arpframe))

	return True

