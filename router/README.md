# Documentation to set up a Raspberry Pi 3, Model B, Vi 2 as a router + server for alterspace

Download full rasbian stretch from here: [2018-11-13-raspbian-stretch-full.zip][dl].

[dl]:https://downloads.raspberrypi.org/raspbian_full/images/raspbian_full-2018-11-15/2018-11-13-raspbian-stretch-full.zip

Follow the [installation guide (linked to linux guide)][guide].

[guide]:https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

Set up sshd:

    sudo systemctl enable ssh
    sudo systemctl start ssh
    sudo systemctl status ssh

If you check the status and there was something along the lines of
`error: /etc/ssh/ssh_host_rsa_key` not readable, you will have to run:

    sudo systemctl stop ssh
    sudo ssh-keygen -A
    sudo systemctl start ssh
    sudo systemctl status ssh

You can also manually generate the host keys, this is just a more
granular version of `sudo ssh-keygen -A`.

## Setting up a wireless network on your pi


**BETTER TUTORIAL HERE: https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software**
BUT BUILT-IN WIFI CHIP DOESN'T SUPPORT MONITOR MODE!
https://raspberrypi.stackexchange.com/questions/45274/kali-linux-wifi-monitor-mode

[How-To: Turn a Raspberry Pi into a WiFi router][router]
([permalink](https://perma.cc/LRT4-9KSB)) is the guide followed for
this. It's pretty old (2013) so here's roughly an update version:

[router]: https://raspberrypihq.com/how-to-turn-a-raspberry-pi-into-a-wifi-router/

- **hostapd**: HostAPD is a user space daemon for access point and
  authentication servers. That means it can will turn your Raspberry Pi
  into a access point that other computers can connect to. It will also
  handle security such that you can setup a WiFi password.

- **isc-dhcp-server**: isc-dhcp-server is the Internet Systems
  Consortium’s implementation of a DHCP server. A DHCP server is
  responsible for assigning addresses to computers and devices connection
  to the WiFi access point.

Install this software with the following:

    sudo apt install isc-dhcp-server hostapd
    # Versions:
    # isc-dhcp-server 4.3.5-3 (version from sudo apt search)
    # hostapd v2.4

Here are some optional dev tools to make things easier:

    sudo apt install nginx mosh neovim diceware
    # Versions:
    # nginx 1.10.3
    # mosh 1.2.6
    # nvim 0.1.7
    # diceware 0.9.1

Continuing with the guide, configure the DHCP server by editing
`/etc/dhcp/dhcpd.conf`:

    sudo nvim /etc/dhcp/dhcpd.conf

Find the following section and comment it out by placing a hashtag at
the beginning of the line.

    option domain-name "example.org";
    option domain-name-servers ns1.example.org, ns2.example.org;

Next find the section below and un-comment the word authoritative
(remove hastag):

    # If this DHCP server is the official DHCP server for the local
    # network, the authoritative directive should be uncommented.
    #authoritative;

Next we need to define the network and network addresses that the DHCP
server will be serving. This is done by adding the following block of
configuration to the end of file:

    subnet 192.168.10.0 netmask 255.255.255.0 {
      range 192.168.10.10 192.168.10.20;
      option broadcast-address 192.168.10.255;
      option routers 192.168.10.1;
      default-lease-time 600;
      max-lease-time 7200;
      option domain-name "local-network";
      option domain-name-servers 1.1.1.1, 8.8.8.8, 8.8.4.4;
    }

This will enable the DHCP server to hand out the ip addresses from
192.168.10.10 to 192.168.10.20 in its own local network. People who
are skilled in network configuration can change these values if they
wish to use some other network addresses and/or other DNS servers. This
configuration will use Cloudflare's encrypted DNS (1.1.1.1), followed by
the Google DNS servers at 8.8.8.8 and 8.8.4.4.

Next file to edit is `/etc/default/isc-dhcp-server`:

    sudo nvim /etc/default/isc-dhcp-server

Scroll down to the line saying interfaces and update the line with your
wireless interface:

    INTERFACES="wlan0"

or

    INTERFACESv4="wlan0"

Depending on your version of `isc-dhcp-server`. We won't look into
managing an IPv6 address space here.

Note that your wireless interface many not be `wlan0`. You can find out
what yours is called by finding an active entry in `iwconfig` or by
checking out `ifconfig`.

This will make the DHCP server hand out network addresses on the
wireless interface. Save the file and exit.

The last step in configuring the DHCP server is to configure a static
ip address for the wireless network adapter. This is done in the file
`/etc/network/interfaces` -- before opening it make sure the WLAN interface
is down.

    sudo ifdown wlan0

Edit `/etc/network/interfaces` to look like the following:

    # interfaces(5) file used by ifup(8) and ifdown(8)

    # Please note that this file is written to be used with dhcpcd
    # For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

    auto lo
    iface lo inet loopback

    auto eth0
    iface eth0 inet dhcp

    allow-hotplug wlan0

    iface wlan0 inet static
      address 192.168.10.1
      netmask 255.255.255.0

This will make the wireless adapter take the address 192.168.10.1 in our
new local network.

This concludes the setup of the DHCP server – however we still cannot
connect to our new network because we have not setup the access point
yet. This is done by configuring the hostapd application.

## Configuring HostAPD

To configure HostAPD, open the file called `/etc/hostapd/hostapd.conf`:

    sudo nvim /etc/hostapd/hostapd.conf

This file may not exist. The standard configuration will create a new
wireless network called wifi with the password YourPassPhrase. You can
change the parameter “ssid=wifi” to the SSID wifi name you want and the
parameter “wpa_passphrase=YourPassPhrase” to your own password.

In this setup no `/etc/hostapd/hostapd.conf` file was created. I found a
small config to go off of [from the internet][hostapd-conf]:

[hostapd-conf]:http://blog.fraggod.net/2017/04/27/wifi-hostapd-configuration-for-80211ac-networks.html

    # https://w1.fi/cgit/hostap/plain/hostapd/hostapd.conf
    ssid=my-test-ap
    wpa_passphrase=set-ap-password

    country_code=US
    # ieee80211d=1
    # ieee80211h=1

    interface=wlan0
    driver=nl80211

    wpa=2
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP

    logger_syslog=0
    logger_syslog_level=4
    logger_stdout=-1
    logger_stdout_level=0

    hw_mode=a
    ieee80211n=1
    require_ht=1
    ieee80211ac=1
    require_vht=1

    vht_oper_chwidth=1
    channel=36
    vht_oper_centr_freq_seg0_idx=42

This concludes the configuration of our access point software HostAPD. Next up is enabling NAT.

## Enable NAT

The last step before we can start the access point is setting up Network
Address Translation (NAT). This will make sure that our network traffic
will be able to reach the internet using the Raspberry Pi’s Ethernet
cable connection to your internet router.

Open `/etc/sysctl.conf`:

    sudo nvim /etc/sysctl.conf

Scroll down to uncomment (or add) the line:

    net.ipv4.ip_forward=1

To start translation right away by running:

    sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

Start the wireless network by running:

    sudo ifup wlan0

Next step is setting up the actual translation between the ethernet port called eth0 and the wireless card called wlan0.

    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

To persist the iptables (FIXME: this seems a bit hacky), run the following command:

    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

and add the following to the end of `/etc/network/interfaces` to restore
the configuration when the network interface comes up:

    up iptables-restore < /etc/iptables.ipv4.nat

With the NAT configured it is now time to run your access point for the first time.

# Starting your wireless router.

You are now ready to start the DHCP server and the HostAPD access point
application. You can do this either by restarting, or by running:

    sudo systemctl restart isc-dhcp-server.service
    sudo systemctl restart hostapd.service

At this point you should be able to find your wireless network on your
laptop and connect to it and the internet!
