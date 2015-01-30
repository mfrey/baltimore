#!/usr/bin/env python2.7

import socket
import os.path
import argparse

class TestbedSetup:
    def __init__(self, interface):
        self.interface_name = interface
        self.commands = []

        chan = self.channel(self.interface_name)
        essid = self.cell_id(self.interface_name)

        self.commands.append("ifconfig " + self.interface_name + " down")
        self.commands.append("ifdown " + self.interface_name)

        self.commands.append("iwconfig " + self.interface_name + " mode ad-hoc")
        self.commands.append("iwconfig " + self.interface_name + " essid des-mesh" + str(chan))
        self.commands.append("iwconfig " + self.interface_name + " channel " + str(chan))
        self.commands.append("iwconfig " + self.interface_name + " ap " + essid)
        self.commands.append("iwconfig " + self.interface_name + " txpower auto")
        self.commands.append("iwconfig " + self.interface_name + " rate 6M")
        self.commands.append("ifconfig " + self.interface_name + " $(calc_ip " + self.interface_name[-1] + ") netmask 255.255.0.0")

    def channel(self, interface_name):
        return {'wlan0': 14, 'wlan1': 36, 'wlan2': 40 }.get(interface_name, 14)

    def cell_id(self, interface_name):
        return {'wlan0': '16:EB:FF:18:C8:6F', 'wlan1': '46:44:4B:28:57:41', 'wlan2': '8A:BF:D2:99:8B:45' }.get(interface_name, 'aa:aa:aa:aa:aa:aa')

    def set_up_ara_configuration(self):
        directory = '/tmp'
        file_name = directory + sockt.gethostname() + '.conf'

        if not self.ara_configuration_exists(file_name):
            self.write_ara_configuration(file_name)

    def ara_configuration_exists(self, file_name):
        return os.path.isfile(file_name)

    def write_ara_configuration(self, file_name):
        pipe = subprocess.Popen(['calc_ip','4'], stdout=subprocess.PIPE)
        output, error = p.communicate()
        tap_address = output.decode('utf-8').rstrip()
        # todo: fixme
        tap_subnet_mask = '255.255.0.0'

        with open(file_name, 'w') as ara_configuration:
            ara_configuration.write('interface sys tap0' + tap_address + ' ' + tap_subnet_mask)
            ara_configuration.write('interface mesh wlan0')


def main():
    parser = argparse.ArgumentParser(description='testbedsetup - a setup script for the DES testbed')
    parser.add_argument('-i', dest='interface', type=str, default="", action='store', help='the interface which should be configured')
    arguments = parser.parse_args()

    if arguments.interface != "":
        testbed_setup = TestbedSetup("wlan0")

if __name__ == "__main__":
    main()
