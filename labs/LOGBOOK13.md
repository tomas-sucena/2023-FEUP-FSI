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

