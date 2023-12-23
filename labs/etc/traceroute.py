#!/usr/bin/env python3
import sys
from scapy.all import *

a = IP(dst=sys.argv[1], ttl=1)
# NOTE: sys.argv[0] -> program name
#       sys.argv[1] -> first argument

while True:
    packet = a / ICMP()
    reply = sr1(packet, timeout=1, verbose=0)
    
    # verify if the TTL was exceeded
    if reply == None or (reply[ICMP].type == 11 and reply[ICMP].code == 0): 
        a.ttl += 1
        continue

    break
    
print("Distance: ", a.ttl)
