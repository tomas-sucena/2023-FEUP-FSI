#!/usr/bin/env python3
from scapy.all import *

def send_reply(packet):
	# verify if the packet is an ICMP echo request
	if packet[ICMP].type != 8:
		return
		
	# create the IP object
	ip = IP(src = packet[IP].dst, dst = packet[IP].src)
	
	# create the ICMP object
	icmp = ICMP(type = 0, id = packet[ICMP].id, seq = packet[ICMP].seq)
	
	# fetch the data
	data = packet[Raw].load
	
	# create and send the reply		
	reply = ip / icmp / data
	send(reply, verbose = 0)

packet = sniff(iface='br-a0c2e1a6c461', filter='icmp', prn=send_reply)
