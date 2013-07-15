#!/usr/bin/env python2.7

from pythonwifi import iwlibs

class TestbedSetup:
    def __init__(self, interface):
        self.interface_name = interface

    def channel(self, interface_name):
        return {'wlan0': 14, 'wlan1': 36, 'wlan2': 40 128 }.get(interface_name, 14)

    def cell_id(self, interface_name):
        return {'wlan0': '16:EB:FF:18:C8:6F', 'wlan1': '46:44:4B:28:57:41', 'wlan2': '8A:BF:D2:99:8B:45' }.get(iface, 'aa:aa:aa:aa:aa:aa')

    def set_up_interface(self):
        chan = self.channel(self.interface_name)
        essid = self.cell_id(self.interface_name)

        subprocess.call("ifconfig " + self.interface_name + " down", shell=True)
        subprocess.call("ifdown " + self.interface_name, shell=True)

        subprocess.call("iwconfig " + self.interface_name + " mode ad-hoc", shell=True)
        subprocess.call("iwconfig " + self.interface_name + " essid des-mesh" + str(chan), shell=True)
        subprocess.call("iwconfig " + self.interface_name + " channel " + str(chan), shell=True)
        subprocess.call("iwconfig " + self.interface_name + " ap " + essid, shell=True)
        subprocess.call("iwconfig " + self.interface_name + " txpower auto", shell=True)
        subprocess.call("iwconfig " + self.interface_name + " rate 6M", shell=True)
        subprocess.call("ifconfig " + self.interface_name + " $(calc_ip " + interface_name[-1] + ") netmask 255.255.0.0", shell=True)

if __name__ == "__main__":
    testbed_setup = TestbedSetup("wlan0")
    testbed_setup.set_up_interface()
