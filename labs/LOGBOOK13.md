# Packet Sniffing and Spoofing

The objective of this lab was to understand the following **network communication** threats:

* **Sniffing**

> **Packet sniffing** is the practice of detecting and assessing data sent over a network.

The most popular tool for sniffing is [Wireshark](https://www.wireshark.org/).

* **Spoofing**

> **Packet spoofing** is the creation of Internet Protocol (IP) packets with a modified <ins>source address</ins> in order to either conceal the identity of the sender or to impersonate another computing system.

**Note:** While not directly related, <ins>spoofing</ins> is frequently used in <ins>Man-in-the-Middle</ins> attacks.

# Setup

Before moving on to the tasks themselves, we had to properly set up our environment. We had to use three machines that were connected to the same LAN as illustrated below:

![Alt text](images/13-1.png)

All the attacks were performed on the attacker machine, while the other two were merely represented the user machines. 

Thankfully, the guide provided a `docker-compose.yml` file that created the necessary containers, as well as the network which connected them. The IP prefix for said network was **10.9.0.0/24**. 

Additionally, the guide prompted us to search for the name of the corresponding **network interface** on our virtual machine, since we would require it for the programs we would write. We did so by executing the `ifconfig` command.

> `ifconfig` is a Linux command that displays the current configuration of the **network interface** of the system. It can also be used to change them.

After setting up the containers, we ran `ifconfig`. The guide specified that the IP address assigned to our virtual machine was **10.9.0.1**, so we looked for it. Luckily for us, we didn't have to search much, because it was the first entry output by the command:

![Alt text](images/13-2.png)

We found the name of our network interface: **br-a0c2e1a6c461**. With that, we could move on the tasks.

**Note:** Throughout this entire lab, we relied on <ins>Scapy</ins>.

> **Scapy** is a network analysis tool that can be also used as a building block to construct other tools.

## Task 1.1: Sniffing Packets

Our first task was to sniff the packets on our network interface. To that end, we used the following Python program provided by the guide:

```Python
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
    pkt.show()

pkt = sniff(iface='br-a0c2e1a6c461', filter='icmp', prn=print_pkt)
```

The `iface` parameter establishes the network interface we wanted to sniff, so we filled it with the name we [previously](#setup) discovered.

**Note:** In the above program, for each packet, the callback function <ins>"print_pkt()"</ins> was invoked, meaning we did not have to explicitly call it.

### 1.1A: Changing the Priviliges

We were tasked with running this script twice: one with the **root** privilege and one without it. As such, we placed the script in a new file - "sniffer.py" - and made it executable so we could reuse it.

```bash
$ chmod a+x sniffer.py
```

To test if we could sniff packets, we had to first send some through the network. To that end, we used the `ping` command.

> `ping` is a Linux command used to check the **network connectivity** between two systems, which can be two hosts or a host and a server.

We opted to send the `ping` command in host A to communicate with host B like so:

```bash
$ ping 10.9.0.6
```

The results of our experiment can be found below:

| Root privilege? | Results          | Conclusion |
|-----------------|------------------|------------|
| Yes | ![Alt text](images/13-3.png) | The packets were sniffed. |
| No  | ![Alt text](images/13-4.png) | The packets were <ins>not</ins> sniffed, because this operation requires **elevated privileges**. |

