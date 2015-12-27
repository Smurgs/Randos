import random
import struct
import socket
import os


def ping_packet():
    """ Return list of ICMP echo request packet and 
    the data that is to be echoed.
    """
    
    # Data fields
    request_type = 8
    code = 0
    checksum = 0
    identifier = os.getpid() & 0xffff
    sequence_number = 3     # Static seq number, any will do
    data = 31*7*92 + random.random()     # Message to be echoed back in reply
    
    # Generate temp packet used to calc checksum
    packet = struct.pack("bbHHHd", request_type, code, checksum, identifier, sequence_number, data)
    
    # Calculate checksum
    sum_of_words = 0
    for i in range(0,len(packet),2):
        sum_of_words += packet[i]*256 + packet[i+1]
    a = sum_of_words + (sum_of_words>>16)   # Carry over anything over 16bits
    b = a & 0xffff      # Get rid of an bits past 16th
    checksum = b ^ 0xffff      # Take 1's complement
    
    # Recreate packet with checksum
    packet = struct.pack("bbHHHd", request_type, code, checksum, identifier, sequence_number, data)
    




# START OF MAIN
ping_packet()
