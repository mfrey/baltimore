#!/usr/bin/env python3

import argparse

from subprocess import call

class TestbedSetup:
    def __init__(self, interface):
        self.interface_name = interface

    def channel(self, interface_name):
        return {'wlan0': 14, 'wlan1': 36, 'wlan2': 40 }.get(interface_name, 14)

    def cell_id(self, interface_name):
        return {'wlan0': '16:EB:FF:18:C8:6F', 'wlan1': '46:44:4B:28:57:41', 'wlan2': '8A:BF:D2:99:8B:45' }.get(interface_name, 'aa:aa:aa:aa:aa:aa')

    def set_up_interface(self):
        chan = self.channel(self.interface_name)
        essid = self.cell_id(self.interface_name)

        call("ifconfig " + self.interface_name + " down", shell=True)
        call("ifdown " + self.interface_name, shell=True)

        call("iwconfig " + self.interface_name + " mode ad-hoc", shell=True)
        call("iwconfig " + self.interface_name + " essid des-mesh" + str(chan), shell=True)
        call("iwconfig " + self.interface_name + " channel " + str(chan), shell=True)
        call("iwconfig " + self.interface_name + " ap " + essid, shell=True)
        call("iwconfig " + self.interface_name + " txpower auto", shell=True)
        call("iwconfig " + self.interface_name + " rate 6M", shell=True)
        call("ifconfig " + self.interface_name + " $(calc_ip " + self.interface_name[-1] + ") netmask 255.255.0.0", shell=True)

def main():
    parser = argparse.ArgumentParser(description='testbedsetup - a setup script for the DES testbed')
    parser.add_argument('-i', dest='interface', type=str, default="", action='store', help='the interface which should be configured')
    arguments = parser.parse_args()

    if arguments.interface != "":
        testbed_setup = TestbedSetup("wlan0")
        testbed_setup.set_up_interface()

if __name__ == "__main__":
    main()
